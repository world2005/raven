/*
 *  distributionFunctions.h
 *
 *  Created on: April 28, 2012
 *      Author: MANDD
 *
 *      Tests      : None for the custom
 *
 *      Problems   : None
 *      Issues      : None
 *      Complaints   : None
 *      Compliments   : None
 *
 *      source: Numerical Recipes in C++ 3rd edition
 *
 */

#ifndef DISTRIBUTIONFUNCTIONS_H_
#define DISTRIBUTIONFUNCTIONS_H_


#include <sstream>
#include <fstream>
#include <ctime>
#include <cstdlib>
#include <vector>
#include <stdio.h>
#include <iostream>
#include <string>
#include <iostream>
#include <stdio.h>
#include <math.h>
#include <cmath>   // to use erfc error function
#include <ctime>   // for rand() and srand()


//#include "distribution_1D.h"

using namespace std;

void nrerror(const char error_text[]);
   /* void nrerror(const char error_text[]){               // added const to avoid "warning: deprecated conversion from string constant to *char */
   /* /\* Numerical Recipes standard error handler *\/ */
   /*    fprintf(stderr,"Numerical Recipes run-time error...\n"); */
   /*    fprintf(stderr,"%s\n",error_text); */
   /*    fprintf(stderr,"...now exiting to system...\n"); */
   /* } */

double gammp(double a, double x);

   /* double gammp(double a, double x){ */
   /* /\* high level function for incomplete gamma function *\/ */
   /*    void gcf(double *gammcf,double a,double x,double *gln); */
   /*    void gser(double *gamser,double a,double x,double *gln); */
   /*    double gamser,gammcf,gln; */
   /*    if(x < 0.0 || a <= 0.0) nrerror("Invalid arg in gammp"); */
   /*    if(x < (a+1.0)){ */
   /* /\* here I change routine so that it returns \gamma(a,x) */
   /*    or P(a,x)-just take out comments to get P(a,x) vs \gamma(a,x)- */
   /*    to get latter use the exp(log(.)+gln) expression *\/ */
   /*      gser(&gamser,a,x,&gln); */
   /* //      return exp(log(gamser)+gln); */
   /*      return gamser; */
   /*    } */
   /*    else{ */
   /*      gcf(&gammcf,a,x,&gln); */
   /* //      return exp(log(1.0-gammcf)+gln); */
   /*      return 1.0-gammcf; */
   /*    } */
   /* } */

double loggam(double xx);
   /* double loggam(double xx) */
   /* { */
   /*    double x,y,tmp,ser; */
   /*    static double cof[6]={76.18009172947146, -86.50532032941677, */
   /*      24.01409824083091,-1.231739572450155, 0.001208650973866179, */
   /*      -5.395239384953e-006}; */
   /*    int j; */
   /*    y=x=xx; */
   /*    tmp=x+5.5; */
   /*    tmp -= (x+0.5)*log(tmp); */
   /*    ser=1.000000000190015; */
   /*    for(j=0;j<=5;j++) ser += cof[j]/++y; */
   /*    return -tmp+log(2.506628274631*ser/x); */
   /* } */

   #define ITMAX 100
   #define EPSW 3.0e-7

void gser(double *gamser,double a,double x,double *gln);
   /* void gser(double *gamser,double a,double x,double *gln){ */
   /*    int n; */
   /*    double sum,del,ap; */
   /*    *gln=loggam(a); */
   /*    if(x <= 0.0){ */
   /*      if(x < 0.0) nrerror("x less than 0 in routine gser"); */
   /*      *gamser=0.0; */
   /*      return; */
   /*    } */
   /*    else{ */
   /*      ap=a; */
   /*      del=sum=1.0/a; */
   /*      for(n=1;n<=ITMAX;n++){ */
   /*        ++ap; */
   /*        del *= x/ap; */
   /*        sum += del; */
   /*        if(fabs(del) < fabs(sum)*EPSW){ */
   /*          *gamser=sum*exp(-x+a*log(x)-(*gln)); */
   /*          return; */
   /*        } */
   /*      } */
   /*      nrerror("a too large, ITMAX too small in routine gser"); */
   /*      return; */
   /*    } */
   /* } */


   #define FPMIN 1.0e-30

void gcf(double *gammcf,double a,double x,double *gln);
   /* void gcf(double *gammcf,double a,double x,double *gln){ */
   /*    int i; */
   /*    double an,b,c,d,del,h; */
   /*    *gln=loggam(a); */
   /*    b=x+1.0-a; */
   /*    c=1.0/FPMIN; */
   /*    d=1.0/b; */
   /*    h=d; */
   /*    for(i=1;i<=ITMAX;i++){ */
   /*      an = -i*(i-a); */
   /*      b += 2.0; */
   /*      d=an*d+b; */
   /*      if(fabs(d) < FPMIN) d=FPMIN; */
   /*      c=b+an/c; */
   /*      if(fabs(c) < FPMIN) c=FPMIN; */
   /*      d=1.0/d; */
   /*      del=d*c; */
   /*      h *= del; */
   /*      if(fabs(del-1.0) < EPSW) break; */
   /*    } */
   /*    if(i > ITMAX) nrerror("a too large, ITMAX too small in gcf"); */
   /*    *gammcf=exp(-x+a*log(x)-(*gln))*h; */
   /* } */

   // Gamma function
   // source http://www.crbond.com/math.htm
double gammaFunc(double x);
   /* double gammaFunc(double x){ */
   /*    int i,k,m; */
   /*    double ga,gr,r,z; */

   /*    static double g[] = { */
   /*       1.0, */
   /*       0.5772156649015329, */
   /*       -0.6558780715202538, */
   /*       -0.420026350340952e-1, */
   /*       0.1665386113822915, */
   /*       -0.421977345555443e-1, */
   /*       -0.9621971527877e-2, */
   /*       0.7218943246663e-2, */
   /*       -0.11651675918591e-2, */
   /*       -0.2152416741149e-3, */
   /*       0.1280502823882e-3, */
   /*       -0.201348547807e-4, */
   /*       -0.12504934821e-5, */
   /*       0.1133027232e-5, */
   /*       -0.2056338417e-6, */
   /*       0.6116095e-8, */
   /*       0.50020075e-8, */
   /*       -0.11812746e-8, */
   /*       0.1043427e-9, */
   /*       0.77823e-11, */
   /*       -0.36968e-11, */
   /*       0.51e-12, */
   /*       -0.206e-13, */
   /*       -0.54e-14, */
   /*       0.14e-14}; */

   /*    if (x > 171.0) return 1e308;    // This value is an overflow flag. */
   /*    if (x == (int)x) { */
   /*       if (x > 0.0) { */
   /*          ga = 1.0;               // use factorial */
   /*          for (i=2;i<x;i++) { */
   /*             ga *= i; */
   /*          } */
   /*        } */
   /*        else */
   /*          ga = 1e308; */
   /*     } */
   /*     else { */
   /*       if (fabs(x) > 1.0) { */
   /*          z = fabs(x); */
   /*          m = (int)z; */
   /*          r = 1.0; */
   /*          for (k=1;k<=m;k++) */
   /*             r *= (z-k); */
   /*          z -= m; */
   /*       } */
   /*       else */
   /*          z = x; */
   /*       gr = g[24]; */
   /*       for (k=23;k>=0;k--) */
   /*          gr = gr*z+g[k]; */

   /*       ga = 1.0/(gr*z); */
   /*       if (fabs(x) > 1.0) { */
   /*          ga *= r; */
   /*          if (x < 0.0) */
   /*             ga = -M_PI/(x*ga*sin(M_PI*x)); */
   /*       } */
   /*    } */
   /*    return ga; */
   /* } */


   // Beta function
double betaFunc(double alpha, double beta);
   /* double betaFunc(double alpha, double beta){ */
   /*    double value=gammaFunc(alpha)*gammaFunc(beta)/gammaFunc(alpha+beta); */
   /*    return value; */
   /* } */


   // log gamma using the Lanczos approximation
double logGamma(double x);
   /* double logGamma(double x) { */
   /* const double c[8] = { 676.5203681218851, -1259.1392167224028, */
   /*        771.32342877765313, -176.61502916214059, */
   /*        12.507343278686905, -0.13857109526572012, */
   /*        9.9843695780195716e-6, 1.5056327351493116e-7 }; */
   /* double sum = 0.99999999999980993; */
   /* double y = x; */
   /* for (int j = 0; j < 8; j++) */
   /*   sum += c[j] / ++y; */
   /* return log(sqrt(2*3.14159) * sum / x) - (x + 7.5) + (x + 0.5) * log(x + 7.5); */
   /* } */

   // helper function for incomplete beta
   // computes continued fraction
double betaContFrac(double a, double b, double x);
   /* double betaContFrac(double a, double b, double x) { */
   /*    const int MAXIT = 1000; */
   /*    const double EPS = 3e-7; */
   /*    double qab = a + b; */
   /*    double qap = a + 1; */
   /*    double qam = a - 1; */
   /*    double c = 1; */
   /*    double d = 1 - qab * x / qap; */
   /*    if (fabs(d) < FPMIN) d = FPMIN; */
   /*    d = 1 / d; */
   /*    double h = d; */
   /*    int m; */
   /*    for (m = 1; m <= MAXIT; m++) { */
   /*      int m2 = 2 * m; */
   /*      double aa = m * (b-m) * x / ((qam + m2) * (a + m2)); */
   /*      d = 1 + aa * d; */
   /*      if (fabs(d) < FPMIN) d = FPMIN; */
   /*      c = 1 + aa / c; */
   /*      if (fabs(c) < FPMIN) c = FPMIN; */
   /*      d = 1 / d; */
   /*      h *= (d * c); */
   /*      aa = -(a+m) * (qab+m) * x / ((a+m2) * (qap+m2)); */
   /*      d = 1 + aa * d; */
   /*      if (fabs(d) < FPMIN) d = FPMIN; */
   /*      c = 1 + aa / c; */
   /*      if (fabs(c) < FPMIN) c = FPMIN; */
   /*      d = 1 / d; */
   /*      double del = d*c; */
   /*      h *= del; */
   /*      if (fabs(del - 1) < EPS) break; */
   /*    } */
   /*    if (m > MAXIT) { */
   /*      cerr << "betaContFrac: too many iterations\n"; */
   /*    } */
   /*    return h; */
   /* } */

   // incomplete beta function
   // must have 0 <= x <= 1
double betaInc(double a, double b, double x);
   /* double betaInc(double a, double b, double x) { */
   /*   if (x == 0) */
   /*    return 0; */
   /*   else if (x == 1) */
   /*    return 1; */
   /*   else { */
   /*    double logBeta = logGamma(a+b) - logGamma(a) - logGamma(b) */
   /*      + a * log(x) + b * log(1-x); */
   /*    if (x < (a+1) / (a+b+2)) */
   /*      return exp(logBeta) * betaContFrac(a, b, x) / a; */
   /*    else */
   /*      return 1 - exp(logBeta) * betaContFrac(b, a, 1-x) / b; */
   /*   } */
   /* } */

double normRNG(double mu, double sigma);
   /* double normRNG(double mu, double sigma) { */
   /*    static bool deviateAvailable=false;                 //        flag */
   /*    static float storedDeviate;                        //        deviate from previous calculation */
   /*    double polar, rsquared, var1, var2; */
   /*    //srand(time(NULL)); */
   /*    //srand((unsigned)time(0)); */
   /*    //srand(time(0)); */
   /*    //Ran ran(time(0)); */
   /*    //        If no deviate has been stored, the polar Box-Muller transformation is */
   /*    //        performed, producing two independent normally-distributed random */
   /*    //        deviates.  One is stored for the next round, and one is returned. */
   /*    if (!deviateAvailable) { */

   /*       //        choose pairs of uniformly distributed deviates, discarding those */
   /*       //        that don't fall within the unit circle */
   /*       do { */
   /*          var1=2.0*( double(rand())/double(RAND_MAX) ) - 1.0; */
   /*          var2=2.0*( double(rand())/double(RAND_MAX) ) - 1.0; */

   /*          //var1=2.0*( ran.doub() ) - 1.0; */
   /*          //var2=2.0*( ran.doub() ) - 1.0; */

   /*          rsquared=var1*var1+var2*var2; */
   /*       } while ( rsquared>=1.0 || rsquared == 0.0); */

   /*       //        calculate polar transformation for each deviate */
   /*       polar=sqrt(-2.0*log(rsquared)/rsquared); */

   /*       //        store first deviate and set flag */
   /*       storedDeviate=var1*polar; */
   /*       deviateAvailable=true; */

   /*       //        return second deviate */
   /*       return var2*polar*sigma + mu; */
   /*    } */

   /*    //        If a deviate is available from a previous call to this function, it is */
   /*    //        returned, and the flag is set to false. */
   /*    else { */
   /*       deviateAvailable=false; */
   /*       return storedDeviate*sigma + mu; */
   /*    } */
   /* } */

void LoadData(double** data, int dimensionality, int cardinality, string filename);
   /* void LoadData(double** data, int dimensionality, int cardinality, string filename) { */
   /*   int x, y; */

   /*   ifstream in(filename.c_str()); */

   /*   if (!in) { */
   /*     cout << "Cannot open file.\n"; */
   /*     return; */
   /*   } */

   /*   for (y = 0; y < cardinality; y++) { */
   /*     for (x = 0; x < dimensionality; x++) { */
   /*       in >> data[y][x]; */
   /*     } */
   /*   } */

   /*   in.close(); */
   /* } */

double calculateCustomPdf(double position, double fitting, double** dataSet, int numberSamples);
   /* double calculateCustomPdf(double position, double fitting, double** dataSet, int numberSamples){ */
   /*    double value=-1; */
   /*    double min; */
   /*    double max; */

   /*    for (int i=1; i<numberSamples; i++){ */
   /*       max=dataSet[i][1]; */
   /*       min=dataSet[i-1][1]; */

   /*       if((position>min)&(position<max)){ */
   /*          if (fitting==1) */
   /*             value=dataSet[i-1][2]; */
   /*          else */
   /*             value=dataSet[i-1][2]+(dataSet[i][2]-dataSet[i-1][2])/(dataSet[i][1]-dataSet[i-1][1])*(position-dataSet[i-1][1]); */
   /*       } */
   /*       else */
   /*          perror ("The following error occurred: distribution sampled out of its boundaries"); */
   /*    } */

   /*    return value; */
   /* } */

double calculateCustomCDF(double position, double fitting, double** dataSet, int numberSamples);
   /* double calculateCustomCDF(double position, double fitting, double** dataSet, int numberSamples){ */
   /*    double value=-1; */
   /*    double min; */
   /*    double max; */
   /*    double cumulative=0; */

   /*    for (int i=1; i<numberSamples; i++){ */
   /*       max=dataSet[i][1]; */
   /*       min=dataSet[i-1][1]; */

   /*       if((position>min)&(position<max)){ */
   /*          if (fitting==1) */
   /*             value=cumulative+dataSet[i-1][2]*(position-dataSet[i-1][1]); */
   /*          else{ */
   /*             double pdfValueInPosition =dataSet[i-1][2]+(dataSet[i][2]-dataSet[i-1][2])/(dataSet[i][1]-dataSet[i-1][1])*(position-dataSet[i-1][1]); */
   /*             value=cumulative + (pdfValueInPosition+dataSet[i-1][2])*(position-dataSet[i-1][1])/2; */
   /*          } */
   /*       } */
   /*       else */
   /*          perror ("The following error occurred: distribution sampled out of its boundaries"); */

   /*       if (fitting==1) */
   /*          cumulative=cumulative+dataSet[i-1][2]*(dataSet[i][1]-dataSet[i-1][1]); */
   /*       else */
   /*          cumulative=cumulative+(dataSet[i][2]+dataSet[i-1][2])*(dataSet[i][1]-dataSet[i-1][1])/2; */
   /*    } */

   /*    return value; */
   /* } */

double rk_gauss();
   /* double rk_gauss() { */
   /*    double f, x1, x2, r2; */

   /*    do { */
   /*       x1 = 2.0*rand() - 1.0; */
   /*       x2 = 2.0*rand() - 1.0; */
   /*       r2 = x1*x1 + x2*x2; */
   /*    } */
   /*    while (r2 >= 1.0 || r2 == 0.0); */

   /*    /\* Box-Muller transform *\/ */
   /*    f = sqrt(-2.0*log(r2)/r2); */
   /*    return f*x2; */
   /* } */

double STDgammaRNG(double shape);
   /* double STDgammaRNG(double shape) */
   /* { */
   /*     double b, c; */
   /*     double U, V, X, Y; */

   /*     if (shape == 1.0) */
   /*     { */
   /*         return -log(1.0 - rand()); */
   /*     } */
   /*     else if (shape < 1.0) */
   /*     { */
   /*         for (;;) */
   /*         { */
   /*             U = rand(); */
   /*             V = -log(1.0 - rand()); */
   /*             if (U <= 1.0 - shape) */
   /*             { */
   /*                 X = pow(U, 1./shape); */
   /*                 if (X <= V) */
   /*                 { */
   /*                     return X; */
   /*                 } */
   /*             } */
   /*             else */
   /*             { */
   /*                 Y = -log((1-U)/shape); */
   /*                 X = pow(1.0 - shape + shape*Y, 1./shape); */
   /*                 if (X <= (V + Y)) */
   /*                 { */
   /*                     return X; */
   /*                 } */
   /*             } */
   /*         } */
   /*     } */
   /*     else */
   /*     { */
   /*         b = shape - 1./3.; */
   /*         c = 1./sqrt(9*b); */
   /*         for (;;) */
   /*         { */
   /*             do */
   /*             { */
   /*                 X = rk_gauss(); */
   /*                 V = 1.0 + c*X; */
   /*             } while (V <= 0.0); */

   /*             V = V*V*V; */
   /*             U = rand(); */
   /*             if (U < 1.0 - 0.0331*(X*X)*(X*X)) */
   /*                return (b*V); */
   /*             if (log(U) < 0.5*X*X + b*(1. - V + log(V))) */
   /*                return (b*V); */
   /*         } */
   /*     } */
   /* } */


double gammaRNG(double shape, double scale);
   /* double gammaRNG(double shape, double scale){ */
   /*    double value=scale * STDgammaRNG(shape); */
   /*    return value; */
   /* } */

double betaRNG(double alpha, double beta);
   /* double betaRNG(double alpha, double beta){ */
   /*    // To be updated */
   /*    double value=0; */
   /*    return value; */
   /* } */



#endif /* DISTRIBUTIONFUNCTIONS_H_ */