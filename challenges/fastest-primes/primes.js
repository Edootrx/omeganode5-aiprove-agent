let d='';process.stdin.on('data',c=>d+=c).on('end',()=>{
const N=+d.trim();if(N<2)return console.log(0);
const h=N>>1,s=new Uint8Array(h+1);let cnt=1;
for(let i=3;i*i<=N;i+=2)if(!s[i>>1])for(let j=i*i;j<=N;j+=2*i)s[j>>1]=1;
for(let i=3;i<=N;i+=2)if(!s[i>>1])cnt++;
console.log(cnt);});
