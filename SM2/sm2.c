#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "sm3.c"


//-----------------检验用，输出16进制，每八个一空格-----------------//
big Output(big m)
{
	int i,len,mid;
	len=numdig(m);
	for(i=0;i<len;i++)
	{
		mid=getdig(m,len-i); //getdig?
		printf("%X",mid);
		if(((i+1)%8==0)&&(i!=0)&&((i+1)%64!=0))
			printf("  ");
		if(((i+1)%64==0)&&(i!=0)&&((i+1)!=len))
			printf("\n");
	}
	printf("\n");
	return 0;
}


//-----------------不同长度异或-----------------//
big DiffLenXor(big a,big b)
{
	int len,len1,len2,x,y,z,i;
	big result;
	result=mirvar(0);
	len1=numdig(a);
	len2=numdig(b);
	if(len1>len2)
		len=len1;
	else
		len=len2;
	for(i=1;i<=len;i++){
		x=getdig(a,i);
		y=getdig(b,i);
		z=x^y;
		putdig(z,result,i);
	}
	return result;
}


//-----------------连接两个大数 || -----------------//
big Connect(big x,big y)
{
	big result,A,B;
	int len1,len2,i,n;
	result=mirvar(0);
	A=mirvar(0);
	B=mirvar(0);
	copy(x,A);
	copy(y,B);
	len1=numdig(A);
	len2=numdig(B);
	for(i=0;i<len2;i++)
	{
		sftbit(A,4,A);
		n=getdig(B,len2-i);
		putdig(n,A,1);
	}
	copy(A,result);
	return result;
}



//-----------------char2hex-----------------//
big Char2Hex(char msg[])
{
	int len,i,x,y,z;
	big result;
	result=mirvar(0);
	len=strlen(msg);
	for(i=0;i<len;i++)
	{
		x=msg[i];
		y=x/16;
		z=x%16;
		if(i==0)
		{
			putdig(y,result,1);
			sftbit(result,4,result);
			putdig(z,result,1);
		}
		else
		{
			sftbit(result,4,result);
			putdig(y,result,1);
			sftbit(result,4,result);
			putdig(z,result,1);
		}
	}
	return result;
}



//-----------------hex2char-----------------//
big Hex2Char(big A)
{
	int n,i,j;
	int m[2];
	char c[500];
	int l=0;
	big a;
	a=mirvar(0);
	copy(A,a);
	n=numdig(a);
	for(i=0;i<n;i++)
	{
		m[0]=getdig(a,n-i);
		i=i+1;
		m[1]=getdig(a,n-i);
		j=m[0]*16+m[1];
		c[l]=j;
		l=l+1;
	}
	c[l]='\0';
	puts(c);
	return 0;
}



//-----------------密钥生成函数-----------------//
big KDF(big q,int klen)
{
	big ct,result,mid,one,Ha;
	big H[100];
	int i,n,m,len,j,x;
	ct=mirvar(0);
	result=mirvar(0);
	mid=mirvar(0);
	one=mirvar(1);
	Ha=mirvar(0);
	for(i=0;i<100;i++)
		H[i]=mirvar(0);
	n=klen/256;
	m=klen%256;
	if(m>0)
		n=n+1;
	cinstr(ct,"00000001");
	for(i=0;i<n;i++)
	{
		copy(q,mid);
		len=numdig(ct);
		if(len<8)
		{
			m=8-len;
			for(j=0;j<m;j++)
				sftbit(mid,4,mid);
		}
		for(j=0;j<len;j++)
		{
			sftbit(mid,4,mid);
			x=getdig(ct,len-j);
			putdig(x,mid,1);
		}
		H[i]=Hash(mid);
		add(ct,one,ct);
	}
	n=klen/256;
	m=klen%256;
	if(m==0)
		copy(H[n-1],Ha);
	else{
		for(i=0;i<m/4;i++)
		{
			sftbit(Ha,4,Ha);
			j=getdig(H[n],64-i);
			putdig(j,Ha,1);
		}
	}
	for(i=0;i<n;i++)
		result=Connect(result,H[i]);
	result=Connect(result,Ha);
	return result;
}




int main()
{
	//变量声明
	FILE *fp;
	int klen,len,i,in,len1,len2,len3,w;
	char msg[500];
	miracl *mip = mirsys(2000,16);
	big m,M,p,a,b,n,Gx,Gy,dB,mid,q,zer,one,PBx,PBy,k,C1x,C1y,P1x,P1y,h,EC1,EC2,EC3,PC,t,EC,DC1x,DC1y,DC2x,DC2y;
	big MM,u;
	epoint *G = epoint_init(); //epoint_init()预定义一个素域上的点，默认值为无穷远
	epoint *PB = epoint_init();
	epoint *C1 = epoint_init();
	epoint *S = epoint_init();
	epoint *P1 = epoint_init();
	epoint *DC1 = epoint_init();
	epoint *DC2 = epoint_init();
	m=mirvar(0);
	M=mirvar(0);
	MM=mirvar(0);
	p=mirvar(0);
	a=mirvar(0);
	b=mirvar(0);
	n=mirvar(0);
	Gx=mirvar(0);
	Gy=mirvar(0);
	dB=mirvar(0);
	q=mirvar(2);
	mid=mirvar(0);
	zer=mirvar(0);
	one=mirvar(1);
	PBx=mirvar(0);
	PBy=mirvar(0);
	C1x=mirvar(0);
	C1y=mirvar(0);
	P1x=mirvar(0);
	P1y=mirvar(0);
	k=mirvar(0);
	h=mirvar(0);
	EC1=mirvar(0);
	EC2=mirvar(0);
	EC3=mirvar(0);
	EC3=mirvar(0);
	PC=mirvar(0);
	t=mirvar(0);
	EC=mirvar(0);
	DC1x=mirvar(0);
	DC1y=mirvar(0);
	DC2x=mirvar(0);
	DC2y=mirvar(0);
	u=mirvar(0);
	mip->IOBASE=16;

	//初始化
	fp=fopen("7.txt","r");
	cinstr(p,"FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF");
	cinstr(a,"FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC");
	cinstr(b,"28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93");
	cinstr(Gx,"32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7");
	cinstr(Gy,"BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0");
	cinstr(n,"FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123");

	printf("------------Encryption--------------\n");

	if(fp){
		i=0;
		while(!feof(fp))
		{
			msg[i]=fgetc(fp);
			i++;
		}
		msg[i-1]='\0';
		printf("Message:\n");
		puts(msg);
		M=Char2Hex(msg);
		klen=numdig(M);
		klen=klen*4;
		subtract(n,q,mid);  //mid=n-q
		bigrand(mid,dB);
		printf("dB:\n");
		Output(dB);
		ecurve_init(a,b,p,MR_AFFINE);//定义椭圆参数曲线
		G->marker = MR_EPOINT_NORMALIZED;//定义G点的类型
		PB->marker = MR_EPOINT_NORMALIZED;//定义PB点的类型
		C1->marker = MR_EPOINT_NORMALIZED;
		S->marker = MR_EPOINT_NORMALIZED;
		P1->marker = MR_EPOINT_NORMALIZED;
		DC1->marker = MR_EPOINT_NORMALIZED;
		DC2->marker = MR_EPOINT_NORMALIZED;
		epoint_set(Gx,Gy,0,G);//给G点赋值
		ecurve_mult(dB,G,PB);//倍点运算
		redc(PB->X,PBx); //将PB->X残基转换回正常形式PBx
		redc(PB->Y,PBy); 
		printf("PBx:\n");
		Output(PBx);
		printf("PBy:\n");
		Output(PBy);
		while(1){
			subtract(n,one,mid);
			bigrand(mid,k);
			printf("k:\n");
			Output(k);
			//计算椭圆曲线点C1=[k]G=(x1,y1)
			ecurve_mult(k,G,C1);//倍点运算
			redc(C1->X,C1x); //将PB->X残基转换回正常形式PBx
			redc(C1->Y,C1y);
			printf("x1:\n");
			Output(C1x);
			printf("y1:\n");
			Output(C1y);
			add(p,one,mid);
			divide(mid,n,h);
			ecurve_mult(h,PB,S);//倍点运算
			in=point_at_infinity(S);
			if(in!=0)
			{
				printf("S error!\n");
				return 0;
			}
			ecurve_mult(k,PB,P1);//倍点运算
			redc(P1->X,P1x);//将PB->X残基转换回正常形式PBx
			redc(P1->Y,P1y);
			//计算椭圆曲线点P1=[k]PB=(x2,y2)
			printf("x2:\n");
			Output(P1x);
			printf("y2:\n");
			Output(P1y);
			//printf("klen=%d\n",klen);
			cinstr(PC,"04");
			EC1=Connect(PC,C1x);
			EC1=Connect(EC1,C1y);
			q=Connect(P1x,P1y);
			t=KDF(q,klen);
			//计算t=KDF(x2||y2,klen)
			printf("t:\n");
			Output(t);
			if(compare(t,zer)!=0)
				break;
		}
		EC2=DiffLenXor(M,t);
		//计算C2=M异或t
		mid=Connect(P1x,M);
		mid=Connect(mid,P1y);
		//计算C3=Hash(x2||M||y2)
		//printf("x2||M||y2:\n");
		//Output(mid);
		EC3=Hash(mid);
		//printf("C3:\n");
		//Output(EC3);
		EC=Connect(EC1,EC2);
		EC=Connect(EC,EC3);
		printf("C=C1||C2||C3:\n");
		Output(EC);


		printf("\n\n------------------------Decryption-----------------------\n");


		len=numdig(EC);
		len1=numdig(EC1);
		cinstr(mid,"0");
		for(i=0;i<len1;i++)
		{
			w=getdig(EC,len-i);
			sftbit(mid,4,mid);
			putdig(w,mid,1);
		}
		len=numdig(mid);
		len1=numdig(C1x);
		len2=numdig(C1y);
		for(i=0;i<len2;i++)
		{
			w=getdig(mid,len-len1-1-i);
			sftbit(DC1y,4,DC1y);
			putdig(w,DC1y,1);
		}
		for(i=0;i<len1;i++)
		{
			w=getdig(mid,len-1-i);
			sftbit(DC1x,4,DC1x);
			putdig(w,DC1x,1);
		}
		ecurve_init(a,b,p,MR_AFFINE);
		epoint_set(DC1x,DC1y,0,DC1);//给DC1点赋值
		in=point_at_infinity(DC1);
		if(in!=0)
		{
			printf("C1 error!\n");
			return 0;
		}
		ecurve_mult(h,DC1,S);//倍点运算
		in=point_at_infinity(S);
		if(in!=0)
		{
			printf("S error!\n");
			return 0;
		}
		ecurve_mult(dB,DC1,DC2);//倍点运算
		redc(DC2->X,DC2x); 
		redc(DC2->Y,DC2y);
		printf("x2:\n");
		Output(DC2x);
		printf("y2:\n");
		Output(DC2y);
		mid=Connect(DC2x,DC2y);
		t=KDF(mid,klen);
		printf("t=KDF(x2||y2,klen):\n");
		Output(t);
		if(compare(t,zer)==0)
			printf("t error!\n");
		len=numdig(EC);
		len1=numdig(EC1);
		len2=numdig(EC2);
		cinstr(mid,"0");
		for(i=0;i<len2;i++)
		{
			w=getdig(EC,len-len1-i);
			sftbit(mid,4,mid);
			putdig(w,mid,1);
		}
		MM=DiffLenXor(mid,t);
		printf("M'=C2^t:\n");
		Output(MM);
		cinstr(mid,"0");
		mid=Connect(DC2x,MM);
		mid=Connect(mid,DC2y);
		u=Hash(mid);
		printf("u =Hash(x2||M'||y2):\n");
		Output(u);
		len=numdig(EC);
		len1=numdig(EC1);
		len2=numdig(EC2);
		len3=numdig(EC3);
		cinstr(mid,"0");
		for(i=0;i<len3;i++)
		{
			w=getdig(EC,len-len1-len2-i);
			sftbit(mid,4,mid);
			putdig(w,mid,1);
		}
		i=compare(mid,u);
		if(i!=0)
		{
			printf("u!=C3,error!\n");
			return 0;
		}
		printf("Hex(Message):\n");
		Output(MM);
		printf("Message:\n");
		Hex2Char(MM);
	}
	else{
		printf("File open error!\n");
	}
	return 0;
}