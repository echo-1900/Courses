#include "miracl.h"


//-----------------SM3中的计算Hash--------------//

big XOR(big a,big b){
	big result;
	int i,x,y,z;
	result=mirvar(0);
	for(i=1;i<=8;i++){
		x=getdig(a,i);
		y=getdig(b,i);
		z=x^y;
		putdig(z,result,i);
	}
	return result;
}

big MOVE(big A,int k){
	big a1,a2,result,a;
	a1=mirvar(0);
	a2=mirvar(0);
	a=mirvar(0);
	result=mirvar(0);
	copy(A,a);
	k=k%32;//W[j]为32比特字符
	expb2(32,a1);
	sftbit(a,k,a2);//左移k位
	copy(a2,result);
	divide(result,a1,a1);//右移32位，余数为剩余的32位，商为前k位
	sftbit(a,k-32,a2);//a右移32-k位,qiank
	add(a2,result,result);
	mirkill(a1);
	mirkill(a2);
	return result;
}

big P1(big X){
	big result;
	result=mirvar(0);
	result=XOR(XOR(X,MOVE(X,15)),MOVE(X,23));
	return result;
}

big P0(big X){
	big result;
	result=mirvar(0);
	result=XOR(XOR(X,MOVE(X,9)),MOVE(X,17));
	return result;
}

big ADD(big a,big b){
	big x,result;
	x=mirvar(0);
	result=mirvar(0);
	expb2(32,x);
	add(a,b,result);
	divide(result,x,x);
	mirkill(x);
	return result;
}

big OR(big a,big b){
	big result;
	int i,x,y,z;
	result=mirvar(0);
	for(i=0;i<8;i++){
		x=getdig(a,i+1);
		y=getdig(b,i+1);
		z=x|y;
		putdig(z,result,i+1);
	}
	return result;
}

big AND(big a,big b)
{
	big result;
	int i,x,y,z;
	result=mirvar(0);
	for(i=0;i<8;i++){
		x=getdig(a,i+1);
		y=getdig(b,i+1);
		z=x&y;
		putdig(z,result,i+1);
	}
	return result;
}

big NOT(big a){
	big result;
	int i,x,y;
	result=mirvar(0);
	for(i=0;i<8;i++){
		x=getdig(a,i+1);
		y=~x;
		putdig(y,result,i+1);
	}
	return result;
}

big FF(big X,big Y,big Z,int j)
{
	big result;
	result=mirvar(0);
	if(j<=15)
		result=XOR(XOR(X,Y),Z);
	else
		result=OR(OR(AND(X,Y),AND(X,Z)),AND(Y,Z));
	return result;
}

big GG(big X,big Y,big Z,int j)
{
	big result;
	result=mirvar(0);
	if(j<=15)
		result=XOR(XOR(X,Y),Z);
	else
		result=OR(AND(X,Y),AND(NOT(X),Z));
	return result;
}

big CF(big V,big B1)
{
	int j,i,n;
	big W[68],W1[68],T[64];
	big A,B,C,D,E,F,G,H,result;
	big SS1,SS2,TT1,TT2;
	A=mirvar(0);
	B=mirvar(0);
	C=mirvar(0);
	D=mirvar(0);
	E=mirvar(0);
	F=mirvar(0);
	G=mirvar(0);
	H=mirvar(0);
	result=mirvar(0);
	SS1=mirvar(0);
	SS2=mirvar(0);
	TT1=mirvar(0);
	TT2=mirvar(0);
	for(j=0;j<68;j++)
		W[j]=mirvar(0);
	for(j=0;j<68;j++)
		W1[j]=mirvar(0);
	for(j=0;j<68;j++)
		T[j]=mirvar(0);
	n=(512/16)/4;
	for(j=0;j<16;j++)
		for(i=0;i<n;i++)
			putdig(getdig(B1,n*(16-j-1)+i+1),W[j],i+1);
	for(j=16;j<68;j++)
	{
		W[j]=XOR(XOR(P1(XOR(W[j-16],XOR(W[j-9],MOVE(W[j-3],15)))),MOVE(W[j-13],7)),W[j-6]);
	}
	for(j=0;j<64;j++)
		W1[j]=XOR(W[j],W[j+4]);

	for(i=0;i<8;i++)
		putdig(getdig(V,i+1+7*8),A,i+1);
	for(i=0;i<8;i++)
		putdig(getdig(V,i+1+6*8),B,i+1);
	for(i=0;i<8;i++)
		putdig(getdig(V,i+1+5*8),C,i+1);
	for(i=0;i<8;i++)
		putdig(getdig(V,i+1+4*8),D,i+1);
	for(i=0;i<8;i++)
		putdig(getdig(V,i+1+3*8),E,i+1);
	for(i=0;i<8;i++)
		putdig(getdig(V,i+1+2*8),F,i+1);
	for(i=0;i<8;i++)
		putdig(getdig(V,i+1+1*8),G,i+1);
	for(i=0;i<8;i++)
		putdig(getdig(V,i+1+0*8),H,i+1);
	for(j=0;j<64;j++)
	{
		if(j<=15)
			cinstr(T[j],"79cc4519");
		else
			cinstr(T[j],"7a879d8a");
	}

	for(j=0;j<64;j++)
	{
		SS1=MOVE(ADD(ADD(MOVE(A,12),E),MOVE(T[j],j)),7);
		SS2=XOR(SS1,MOVE(A,12));
		TT1=ADD(ADD(ADD(FF(A,B,C,j),D),SS2),W1[j]);
		TT2=ADD(ADD(ADD(GG(E,F,G,j),H),SS1),W[j]);
		D=C;
		C=MOVE(B,9);
		B=A;
		A=TT1;
		H=G;
		G=MOVE(F,19);
		F=E;
		E=P0(TT2);
	}
	add(A,result,result);
	sftbit(result,32,result);
	add(B,result,result);
	sftbit(result,32,result);
	add(C,result,result);
	sftbit(result,32,result);
	add(D,result,result);
	sftbit(result,32,result);
	add(E,result,result);
	sftbit(result,32,result);
	add(F,result,result);
	sftbit(result,32,result);
	add(G,result,result);
	sftbit(result,32,result);
	add(H,result,result);
	for(i=1;i<=64;i++){
		putdig(getdig(V,i)^getdig(result,i),V,i);
	}
	for(i=0;i<68;i++)
		mirkill(W[i]);
	for(i=0;i<68;i++)
		mirkill(W1[i]);
	for(i=0;i<64;i++)
		mirkill(T[i]);
	return V;
}

big Hash(big M){
	int len,j,n,k,i;
    miracl *mip = mirsys(5000,16);
	big V,B,m;
	V=mirvar(0);
	B=mirvar(0);
	m=mirvar(0);
	mip->IOBASE=16;
	cinstr(V,"7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e");
	copy(M,m);
	len=numdig(m);//计算消息m的位数
	sftbit(m,4,m);//一个字符四个比特，所以要移位4比特；将大数x移位n位得到z
	putdig(8,m,1);//将大数x的n2位换成n1;因为普通为小端字符所以将第一位改成8(1000)
	j=0;
	n=4*len+68;
	while(n>512){
		j=j+1;
		n=n-512;
	}
	k=512*j+(512-68-4*len);
	sftbit(m,k,m);//补充0
	sftbit(m,64,m);
	incr(m,4*len,m);//将消息的长度加入到末尾，即m=m+4*len
	n=numdig(m)*4/512;
	for(i=0;i<n;i++)//进行迭代压缩
	{
		for(k=(n-i-1)*512/4;k<(n-i)*512/4;k++)//分组，求B(i)
			putdig(getdig(m,k+1),B,k-(n-i-1)*512/4+1);//putdig是对大数进行操作的，sftdig是对比特进行操作的
				//此处进行反操作(一般的是后边的放在第一个，此处第一个放在第一个);
		V=CF(V,B);
	}
	return V;
}