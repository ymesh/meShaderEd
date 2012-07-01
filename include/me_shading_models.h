#ifndef ME_SHADING_MODELS_H
#define ME_SHADING_MODELS_H
#include "me_util.h"
/*-----------------------------------------------------------*/
/* Specular        */
/*-----------------------------------------------------------*/
color meSpecular( 
      uniform string category;
      color SpecColor;
      float Ks;
      float roughness; 
      )
{
 
  extern normal N;
  extern vector L, I;
  extern point P;
  extern color Cl;
  color result = 0;
  
  normal Nf = faceforward( normalize(N), I );
  vector Nn = normalize(N);
  color spec = 0;
  
  /* spec =  specular(Nf, -normalize(I), roughness); */
  P = P; /* dirty light cache  , "lightcache", "refresh" */ 
  illuminance( category, P, Nf, PI/2 ) 
  { 
    float nonspec = 0;
    lightsource("__nonspecular", nonspec);
    if (nonspec < 1)
      spec += (1-nonspec) * Cl * specularbrdf(normalize(L), Nf, -normalize(I), roughness);
  }
  
  result = Ks * spec * SpecColor;
  return result;
}
/*-----------------------------------------------------------
 Specularity with close falloff for a wet apearance        
-----------------------------------------------------------*/
color meGlossySpecular(
      uniform string category;
      color SpecColor;
      float Ks;
      float roughness;
      float sharpness;
      )
{
  color GlossyColor( uniform string category; normal N; vector V; float roughness, sharpness; )
  {
    color C = 0;
    float w = .18 * (1-sharpness);
    extern point P;
    
    illuminance (P, N, PI/2) 
    {
      /* Must declare extern L & Cl because we're in a function */
      extern vector L;  
      extern color Cl; 
      float nonspec = 0;
      lightsource ("__nonspecular", nonspec);
      if (nonspec < 1) 
      {
         vector H = normalize(normalize(L)+V);
         C += Cl * ( (1-nonspec) * smoothstep (.72-w, .72+w, pow(max(0,N.H), 1/roughness)) );
       }
     }
     return C;
   }
   extern normal N;
   extern vector I;
   normal Ns = meShadingNormal( N );
   color spec = SpecColor * Ks * GlossyColor( category, Ns, -normalize(I), roughness, sharpness );
   return spec; 
}
/*-----------------------------------------------------------*/

/*-----------------------------------------------------------*/
color meBlinn( uniform string category; 
                color specularColor;
                float Ks;
                float eccentricity, specularRollOff, reflectivity;
             )
{
  
  extern normal N;
  extern point P;
  extern vector L, I;
  extern color Cl;
  color result = 0;
  
  normal Nf = faceforward( normalize(N), I );
  vector R = reflect( normalize(I), Nf);
  
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
  illuminance( category, P, Nf, PI/2 )
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

/*-----------------------------------------------------------
	meDiffuse
	
	This is some mix of standart Pixar Slim Diffuse function  
	and Stefano Tobacco ST_Diffloat templates  
-----------------------------------------------------------*/
color meDiffuse(
      uniform string category;
      float Kd;
      float atten;
      float from;
      float to;
      color coloration; 
      )
{
  extern normal N;
	extern vector I;
	extern point P;
		
	normal Nf = faceforward( normalize(N), I );
	color diffColor = 0;
	color result = 0;
              
	illuminance ( category, P, Nf, PI/2, "lightcache", "refresh" ) 
	{
		float nondiff = 0;
		lightsource("__nondiffuse", nondiff);
		if (nondiff < 1)
			diffColor += ( 1 - nondiff ) * Cl*(Nf.normalize(L));
	}
	
	
	float hueComp = comp( ctransform( "hsv" , diffColor ) , 0 );
	float satComp = comp( ctransform( "hsv" , diffColor ), 1 );
	float lumiComp = comp( ctransform( "hsv" , diffColor ), 2 ); /*  get value component from HSV color space */
	color hsvDiff = color "hsv" ( hueComp, satComp, ( from + ( to - from ) * pow( lumiComp, atten ) ) );
  
	result = coloration * Kd * hsvDiff;
	return result;
}
/*-----------------------------------------------------------
	meWrappedDiffuse
	
	One shotcoming of the traditional lighting model is:
	diffuse falloff too fast. Wrapped Diffuse Lighting model 
	gave the light the ability 	to reach beyond the 90 degree point 
	on the surface of objects, producing softened 
	light, as if simulating an area light. 
	A few of directional lights is sufficient.
	Here is the float function used to vary a colorSpline 
	according to the wrapped diffuse.'said zj, July 26,2002."

-----------------------------------------------------------*/
color meWrappedDiffuse( 
				uniform string category;
				float Kd;
		    float Kw;
		    float att;
		    )
		   
{
	extern vector I;
	extern normal N;
	extern point P;
	
	vector Nn = normalize(N);
	normal Nf = faceforward( normalize(N), I );
	float ang;
	color result = 0;
	
	illuminance( category, P, Nn, PI) 
	{
	 extern vector L;
	 vector Ln = normalize(L);
	 ang = acos(Ln.Nn);
	}
	result = Kd * pow(max((1-ang/(PI*Kw)),0),att);
	return result;
}

/*-----------------------------------------------------------*/

/*-----------------------------------------------------------*/
color meIBI_diff(
  uniform string category;
  float dBlur;
	float Kd;
	normal Ns;
	output varying vector  __L;
  output varying float   __blur; )
{
  extern point P;
  
  color diffuse_color = 0;
  
  __L = Ns;
  __blur = dBlur;
  P = P; /* dirty light cache  , "lightcache", "refresh" */ 
  illuminance ( category, P ) 
  {
    diffuse_color += Cl;
  }     
  return ( diffuse_color * Kd );
}
/*-----------------------------------------------------------*/

/*-----------------------------------------------------------*/
color meIBI_spec(
  uniform string category;
  float rBlur;
	float KrMin;
	float KrMax;
	float IOR;
	normal Ns;
	output varying vector  __L;
  output varying float   __blur; )
{

  extern vector I;
  extern point P;

  float Kr;
	vector R;
	vector V = normalize (I);  
  
  color specular_color = 0;
  
  if(IOR > 0)
	{
	    vector T;
	    float Kt;
	    float f = max(IOR, 1.0e-4);
 		  fresnel (V, Ns, (I.Ns < 0) ? 1.0/f : IOR,	Kr, Kt, R, T);
	    Kr = mix( KrMin, KrMax, Kr );
	}
	else
	{
	    R = reflect(V, Ns);
	    Kr = KrMax;
	}
  
  __L = R;
  __blur = rBlur;
  P = P; /* dirty light cache */
  illuminance ( category, P ) /* , "lightcache", "refresh" */
  {
    specular_color += Cl;
  }     
  return ( specular_color * Kr );
}          

#endif 	    
