// Genera web/index.html protegido con clave común.
// Cifra el script de la app (datos incluidos) con AES-256-GCM; la clave sale de PI_CLAVE (PBKDF2).
// Uso: PI_CLAVE=... node motor/cifrar_web.mjs   (si falta PI_CLAVE, falla a propósito y no publica nada)
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { webcrypto as crypto } from 'node:crypto';
const clave = process.env.PI_CLAVE || '';
if (clave.length < 6) { console.error('Falta PI_CLAVE (mínimo 6 caracteres). No se genera la web.'); process.exit(1); }
const ITER = 250000;
const src = readFileSync(new URL('../salida/app/Pretzhet_Ink_app.html', import.meta.url), 'utf8');
const a = src.lastIndexOf('<script>'), b = src.lastIndexOf('</script>');
if (a < 0 || b < a) { console.error('No encuentro el script de la app.'); process.exit(1); }
const code = src.slice(a + 8, b);
const enc = new TextEncoder();
const salt = crypto.getRandomValues(new Uint8Array(16)), iv = crypto.getRandomValues(new Uint8Array(12));
const km = await crypto.subtle.importKey('raw', enc.encode(clave), 'PBKDF2', false, ['deriveKey']);
const key = await crypto.subtle.deriveKey({ name: 'PBKDF2', salt, iterations: ITER, hash: 'SHA-256' }, km, { name: 'AES-GCM', length: 256 }, false, ['encrypt']);
const ct = new Uint8Array(await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, enc.encode(code)));
const b64 = u => Buffer.from(u).toString('base64');
const gate = `<style>
#gate{position:fixed;inset:0;z-index:200;background:#050F20;display:flex;align-items:center;justify-content:center;padding:16px;font-family:Inter,system-ui,sans-serif}
#gate form{width:100%;max-width:340px;text-align:center;color:#fff}
#gate img{height:56px;margin-bottom:28px}
#gate input{width:100%;box-sizing:border-box;padding:13px 14px;border-radius:10px;border:1px solid #2a3a55;background:#0b1a33;color:#fff;font-size:16px;text-align:center}
#gate input:focus{outline:2px solid #FD513B;border-color:#FD513B}
#gate button{margin-top:12px;width:100%;padding:13px;border:0;border-radius:10px;background:#FD513B;color:#fff;font-size:16px;font-weight:600;cursor:pointer}
#gate p{min-height:20px;margin:10px 0 0;color:#ff9a8c;font-size:14px}
</style>
<div id="gate"><form id="gf"><img id="gl" alt="Escòla"><input id="gp" type="password" placeholder="Clave de acceso" autocomplete="current-password" autofocus><button>Entrar</button><p id="ge"></p></form></div>
<script>
(function(){
var P='${b64(salt)}',V='${b64(iv)}',C='${b64(ct)}',N=${ITER};
var d=function(s){return Uint8Array.from(atob(s),function(c){return c.charCodeAt(0)})};
var l=document.querySelector('.lg2'); if(l) document.getElementById('gl').src=l.src; else document.getElementById('gl').remove();
async function abrir(k){
  var km=await crypto.subtle.importKey('raw',new TextEncoder().encode(k),'PBKDF2',false,['deriveKey']);
  var key=await crypto.subtle.deriveKey({name:'PBKDF2',salt:d(P),iterations:N,hash:'SHA-256'},km,{name:'AES-GCM',length:256},false,['decrypt']);
  var pt=await crypto.subtle.decrypt({name:'AES-GCM',iv:d(V)},key,d(C));
  var s=document.createElement('script'); s.textContent=new TextDecoder().decode(pt);
  document.getElementById('gate').remove(); document.body.appendChild(s);
}
async function probar(k,rec){
  try{ await abrir(k); if(rec){try{localStorage.setItem('pi-clave',k)}catch(e){}} return true }catch(e){ return false }
}
document.getElementById('gf').addEventListener('submit',async function(e){
  e.preventDefault(); var g=document.getElementById('ge'); g.textContent='';
  if(!window.crypto||!crypto.subtle){g.textContent='Este navegador no permite abrir la app (hace falta https).';return}
  g.textContent='Comprobando…';
  if(!(await probar(document.getElementById('gp').value,true))) g.textContent='Clave incorrecta';
});
var k0=null; try{k0=localStorage.getItem('pi-clave')}catch(e){}
if(k0) probar(k0,false).then(function(ok){ if(!ok){try{localStorage.removeItem('pi-clave')}catch(e){}} });
})();
</script>`;
mkdirSync(new URL('../web/', import.meta.url), { recursive: true });
writeFileSync(new URL('../web/index.html', import.meta.url), src.slice(0, a) + gate + src.slice(b + 9));
console.log('web/index.html cifrado,', Math.round(ct.length / 1024), 'KB de datos');
