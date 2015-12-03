#include<bits/stdc++.h>
using namespace std;
char a[100000+10];
char b[100000+10];
char buf[100000+10];
string sa[50];
string sb[50];
int main(int argc,char *argv[]){
    FILE *fin1,*fin2;
    FILE *fout;
    int mode=atoi(argv[1]);
    if(mode==1){
        fin1=fopen("./csv/train.csv","r");
        fin2=fopen("./csv/sample_solution_hd100_train.csv","r");
        fout=fopen("./csv/train_append_dbz.csv","w");
        fprintf(fout,"Id,minutes_past,radardist_km,Ref,Ref_5x5_10th,Ref_5x5_50th,Ref_5x5_90th,RefComposite,RefComposite_5x5_10th,RefComposite_5x5_50th,RefComposite_5x5_90th,RhoHV,RhoHV_5x5_10th,RhoHV_5x5_50th,RhoHV_5x5_90th,Zdr,Zdr_5x5_10th,Zdr_5x5_50th,Zdr_5x5_90th,Kdp,Kdp_5x5_10th,Kdp_5x5_50th,Kdp_5x5_90th,dbz,Expected\n");
    }
    else{
        fin1=fopen("./csv/test.csv","r");
        fin2=fopen("./csv/sample_solution_hd100.csv","r");
        fout=fopen("./csv/test_append_dbz.csv","w");
        fprintf(fout,"Id,minutes_past,radardist_km,Ref,Ref_5x5_10th,Ref_5x5_50th,Ref_5x5_90th,RefComposite,RefComposite_5x5_10th,RefComposite_5x5_50th,RefComposite_5x5_90th,RhoHV,RhoHV_5x5_10th,RhoHV_5x5_50th,RhoHV_5x5_90th,Zdr,Zdr_5x5_10th,Zdr_5x5_50th,Zdr_5x5_90th,Kdp,Kdp_5x5_10th,Kdp_5x5_50th,Kdp_5x5_90th,dbz\n");
    }
    fscanf(fin1,"%s",a);
    fscanf(fin2,"%s",b);

    fscanf(fin2,"%s",b);
    char *ptr;
    int cnta=0,cntb=0,top=0;
    for(int i=0;b[i];i++){
        if(b[i]==','){
            buf[top]='\0';
            sb[cntb++]=buf;
            top=0;
        }
        else buf[top++]=b[i];
    }
    buf[top]='\0';
    sb[cntb++]=buf;

    while(~fscanf(fin1,"%s",a)){
        cnta=top=0;
        for(int i=0;a[i];i++){
            if(a[i]==','){
                buf[top]='\0';
                sa[cnta++]=buf;
                top=0;
            }
            else buf[top++]=a[i];
        }
        buf[top]='\0';
        sa[cnta++]=buf;

        while(sa[0]!=sb[0]){
            fscanf(fin2,"%s",b);
            cntb=top=0;
            for(int i=0;b[i];i++){
                if(b[i]==','){
                    buf[top]='\0';
                    sb[cntb++]=buf;
                    top=0;
                }
                else buf[top++]=b[i];
            }
            buf[top]='\0';
            sb[cntb++]=buf;
        }

        if(mode==1){
            for(int i=0;i<cnta-1;i++){
                if(i!=0)fprintf(fout,",");
                fprintf(fout,"%s",sa[i].c_str());
            }
            fprintf(fout,",%s",sb[1].c_str());
            fprintf(fout,",%s\n",sa[cnta-1].c_str());
        }
        else{
            for(int i=0;i<cnta;i++){
                if(i!=0)fprintf(fout,",");
                fprintf(fout,"%s",sa[i].c_str());
            }
            fprintf(fout,",%s\n",sb[1].c_str());
        }

    }
    puts("finished");

    fclose(fin1);
    fclose(fin2);
    fclose(fout);
    return 0;
}
