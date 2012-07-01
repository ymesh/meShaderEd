#ifndef ME_BLINN_H
#define ME_BLINN_H
#include "me_util.h"
/*-----------------------------------------------------------*/
/* Mimics the Maya Blinn shader                              */
/*-----------------------------------------------------------*/
color meBlinn(
      uniform string category;
      color specularColor;
      float Ks;
      float eccentricity;
      float specularRollOff;
      float reflectivity;
      )
{
	extern normal N;
	extern point P;
	extern vector L, I;
	extern color Cl;
	
	normal Nf = faceforward( normalize(N), I );
	vector R = reflect( normalize(I), Nf);
	
	color result = color( 0 );
	float E;
	color C = 0, Cr = 0;
	vector H, Ln, V, Nn;
	float NH, NH2, NHSQ, Dd, Gg, VN, VH, LN, Ff, tmp;
	float nondiff, nonspec;
	

	if(eccentricity != 1)
		E = 1 / (eccentricity * eccentricity - 1);
	else
		E = -1e5;
	Cr = 0;
	V = normalize(-I);
	VN = V.Nf;
	illuminance( category, P, Nf, 1.57079632679 )
	{
		if( 0 == lightsource("__nonspecular", nonspec) )
			nonspec = 0;
		if( nonspec < 1 )
		{
			Ln = normalize(L);
			H = normalize(Ln+V);
			NH = Nf.H;
			NHSQ = NH * NH;
			NH2 = NH * 2;
			Dd = ( E + 1) / (NHSQ + E);
			Dd *= Dd;
			VH = V.H;
			LN = Ln.Nf;
			if( VN < LN )
			{
				if( VN * NH2 < VH )
					Gg = NH2 / VH;
				else
					Gg = 1 / VN;
			}
			else
			{
				if( LN * NH2 < VH )
					Gg = (LN * NH2) / (VH * VN);
				else
					Gg = 1 / VN;
			}
			/* poor man's Fresnel */
			tmp = pow((1 - VH), 3);
			Ff = tmp + (1 - tmp) * specularRollOff;
			C += Cl * Dd * Gg * Ff;
		
			/* now look for environment reflections.  
				 These are indicated by lights which are specular AND nondiffuse 
			*/
			if( 0 != lightsource("__nondiffuse", nondiff) )
			{
				Cr += ( 1 - nonspec ) * nondiff * Ff * Cl;
			}
		}
	}
		 
	result = Ks * specularColor * ( C + reflectivity * Cr );  
	return result;
}
#endif            
