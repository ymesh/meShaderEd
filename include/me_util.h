#ifndef ME_UTIL_H
#define ME_UTIL_H

color meDesaturate ( color in_color; float dsat )
{
  float lum = .2125*comp(in_color, 0) + .7154*comp(in_color, 1) + .0721*comp(in_color, 2);
	color out_color = mix(color(lum), in_color, dsat);
	
	return out_color;
}	 

color meCmix(color a; color b; color mixture)
{
    return (1 - mixture) * a +  mixture * b;
}

normal meShadingNormal( normal n )
{
  extern vector I;
  normal Nn = normalize( n );
  normal Nf = faceforward( Nn, I, Nn );
  normal Ns = normalize( Nf ); /* shading normal */
  return Ns;
}

/*
 * Build a set of four vectors around a center vector
 * This is necessary for making environment calls inside
 * of a gather loop. If we just used a single vector,
 * we would get derivative information based on neighboring
 * grids, which is not what we want. Instead, we want to
 * do a lookup on a patch of the environment that is inversely
 * related to the number of samples we are using.
 *
 * spread is the halfwidth of the patch we are using
 *
 * This is calculated as a separate function so that it can be
 * called outside of the gather loop (for the sake of optimization).
 */

float
meCalculateEnvSampleArea(
    float hemisphere;
    float numSamples;
    )
{
    return 0.5 * (hemisphere / numSamples);
}

void
meBuildEnvironmentVectors(
    float spread;
    vector dir;
    output vector v1;
    output vector v2;
    output vector v3;
    output vector v4;
    )
{
  vector udir, vdir, wdir;

  // construct basis vectors
  if (abs(xcomp(dir)) > 0 || abs(ycomp(dir)) > 0)
	  // dir ^ z (if valid)
	  udir = normalize(vector (ycomp(dir), -xcomp(dir), 0));
  else
	  // dir ^ x
	  udir = normalize(vector (0, zcomp(dir), -ycomp(dir)));

  // vdir is dir ^ u
  vdir = normalize(dir ^ udir);
  
  // calculate four directions
  vector uspread = spread*udir;
  vector vspread = spread*vdir;
  vector ndir = normalize(dir);
  
  v1 = ndir - uspread - vspread;
  v2 = ndir + uspread - vspread;
  v3 = ndir - uspread + vspread;
  v4 = ndir + uspread + vspread;
}

#endif 	    
