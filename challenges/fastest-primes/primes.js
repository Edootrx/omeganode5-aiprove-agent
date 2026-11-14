const d=require('fs').readFileSync(0,'utf8'),N=+d.trim();
if(N<2){console.log(0);process.exit(0)}
const h=(N-1)>>1,s=new Uint8Array(h+1),r=Math.sqrt(N)|0;
for(let i=3;i<=r;i+=2)if(!s[i>>1]){const st=(i*i)>>1;for(let j=st;j<=h;j+=i)s[j]=1}
let cnt=1;for(let i=1;i<=h;i++)cnt+=1-s[i];
console.log(cnt);
