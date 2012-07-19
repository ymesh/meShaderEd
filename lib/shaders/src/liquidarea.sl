/*
**
** The contents of this file are subject to the Mozilla Public License Version
** 1.1 (the "License"); you may not use this file except in compliance with
** the License. You may obtain a copy of the License at
** http://www.mozilla.org/MPL/
**
** Software distributed under the License is distributed on an "AS IS" basis,
** WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
** for the specific language governing rights and limitations under the
** License.
**
** The Original Code is the Liquid Rendering Toolkit.
**
** The Initial Developer of the Original Code is Colin Doncaster. Portions
** created by Colin Doncaster are Copyright (C) 2002. All Rights Reserved.
**
** Contributor(s): Philippe Leprince.
**
**
** The RenderMan (R) Interface Procedures and Protocol are:
** Copyright 1988, 1989, Pixar
** All Rights Reserved
**
**
** RenderMan (R) is a registered trademark of Pixar
*/

/* ______________________________________________________________________
**
** Liquid Area Light Shader Source
** ______________________________________________________________________
*/



#ifdef PRMAN
normal shadingnormal(normal N) {
  normal Ns = normalize(N);
  uniform float sides = 2;
  uniform float raydepth;
  attribute("Sides", sides);
  rayinfo("depth", raydepth);
  if (sides == 2 || raydepth > 0) Ns = faceforward(Ns, I, Ns);
  return Ns;
}
#else
normal shadingnormal(normal Ne){
	normal Ns;
	uniform float sides = 2;
	attribute("Sides",sides);
	if(sides == 2)	Ns = faceforward(normalize(Ne),I,Ne);
	else			Ns = normalize(Ne);
	return Ns;
}
#endif

/*
 * Simple implementation of a rectangular "pseudo area light".
 * This is an analytic solution to the problem.
 * We use stratified sampling to illuminate the surfaces.
 * Shadows are computed using the transmission shadeop, so
 * shadow-casting objects should be visible to transmission
 * rays. This is potentially expensive.
 * The light uses a named coordinate system to calculate
 * it's geometry. This coordinate system can also be used to
 * render specular reflections in surface shaders using
 * message passing.
 */

light
liquidarea(
      uniform float   intensity     = 1;
      uniform color   lightcolor    = 1;
      uniform float   decay         = 2;
      uniform string  coordsys      = "";
      uniform float   lightsamples  = 32;
      uniform float   doublesided   = 0;
      uniform string  shadowname    = "";
      uniform color   shadowcolor   = 0;
      uniform string  hitmode       = "primitive";

      uniform string  lightmap      = "";
      uniform float   lightmapsaturation  = 2.0;

      uniform float  lightID        = 0;
      uniform string __category     = "";

      output uniform float __nonspecular          = 1;
      output varying float __shadowF              = 0;
      output varying color __shadowC              = 0;
      output varying color __unshadowed_Cl        = 0;
      output uniform float __arealightIntensity   = 0;
      output uniform color __arealightColor       = 0;
)
{
  /* force non-specular */
  __nonspecular = 1;

  /* get the size of the coordinate system */
  uniform float xsize = 1;
  uniform float ysize = 1;
  uniform point P1 = transform( coordsys, point "shader" (1, 1, 1) );
  xsize = 2/xcomp( P1 );
  ysize = 2/ycomp( P1 );

  uniform float xsamples, ysamples, i, j;
  color c, test;
  normal Ns = shadingnormal(N);
  vector len, lnorm, Nl;
  float x, y, dist, dot;
  varying float orient = 1;
  point p;

  /*  stratified sampling approach
   *  we will actually use more samples than the requested number.
   */
  uniform float aspectRatio = xsize / ysize;
  uniform float sqr = sqrt(lightsamples);
  xsamples = min(lightsamples, max( 2, ceil(sqr*aspectRatio) ) );
  ysamples = min(lightsamples, max( 2, ceil(sqr/aspectRatio) ) );
  if ( xsamples == 2 ) ysamples /= 2;
  if ( ysamples == 2 ) xsamples /= 2;

  uniform float totalNbrSamples = xsamples * ysamples;
  varying color finalcolor = 0, unshadowedC = 0, shadowC = 0;

  /* Compute illumination */
  illuminate ( Ps + Ns ) {  /* force execution independent of light location */

    for (j = 0; j < ysamples; j += 1)  {
      for (i = 0; i < xsamples; i += 1)  {

        /* Compute jittered point (x,y) on unit square */
        x = (i + random()) / xsamples;
        y = (j + random()) / ysamples;

        /* Compute point p on rectangle */
        p = point "shader" ((x - 0.5) * xsize, (y - 0.5) * ysize, 0);

        /* Texture lookup for light color */
        //if ( x < 0 || x > 1 ) printf("x = %f   ", x);
        if ( lightmap != "" ) finalcolor = color texture( lightmap, 1-x, 1-y );
        else finalcolor = 1.0;
        finalcolor *= lightcolor;

        /* Compute distance from light point p to surface point Ps */
        len = p - Ps;
        dist = length(len);
        lnorm = len / dist;

        /* luminaire sidedness */
        if ( doublesided == 0 ) {
          Nl = ( p - point "shader" ((x - 0.5) * xsize, (y - 0.5) * ysize, 1) ) ;
          orient = clamp( (Nl.len)/dist, 0, 1);
        }

        /* Compute light from point p to surface point Ps */
        dot = lnorm.Ns;
        if ( orient > 0 ) {

          c = intensity* orient;

          /* distance falloff */
          c *= pow(dist , -decay);

          /* Lambert's cosine law at the surface */
          c *= dot;

          /* color the light */
          c *= finalcolor;

          /* accumulate unshadowed contribution */
          __unshadowed_Cl += c;

          /* raytraced occlusion - only if the point is reasonnably lit */
          if ( shadowname == "raytrace" && (comp(c,0)+comp(c,1)+comp(c,2))>0.005  ) {
            shadowC = transmission(Ps, p, "hitmode", hitmode, "label", "liqAreaLightShad");
            __shadowC += shadowC;
          } else {
            /* No shadowing, so assume visibility for this sample is 1 */
            __shadowC += finalcolor;
          }

        }
      }
    }

    /* saturation control */
    if ( lightmapsaturation != 1.0 ) {
      varying color tmpc = ctransform( "rgb", "hsl", __unshadowed_Cl );
      setcomp( tmpc, 1, comp(tmpc, 1) * lightmapsaturation );
      __unshadowed_Cl = ctransform( "hsl", "rgb", tmpc );
    }
    __unshadowed_Cl /= totalNbrSamples;
    __shadowC /= totalNbrSamples;
#if defined ( AIR ) || defined ( AQSIS )
    Cl = color(mix(comp(shadowcolor,0),comp(__unshadowed_Cl,0),comp(__shadowC,0)),
               mix(comp(shadowcolor,1),comp(__unshadowed_Cl,1),comp(__shadowC,1)),
               mix(comp(shadowcolor,2),comp(__unshadowed_Cl,2),comp(__shadowC,2)));
#else
    Cl = mix( shadowcolor, __unshadowed_Cl, __shadowC );
#endif
  }

  __shadowF = 1 - ( comp(__shadowC, 0)*0.3 + comp(__shadowC, 1)*0.59 + comp(__shadowC, 2)*0.11);
  __arealightIntensity = intensity;
  __arealightColor     = lightcolor;
}
