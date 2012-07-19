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
** Liquid Distant Light Shader Source
** ______________________________________________________________________
*/




light
liquiddistant(
      uniform float intensity = 1;
      uniform color lightcolor = 1;

      string shadowname = "";  /* shadow map name or "raytrace" for traced shadows */
      uniform float shadowbias = 0.01;
      uniform float shadowblur = 0.0;
      uniform float shadowsamples = 16; /* samples or rays */
      uniform float shadowfiltersize = 1;
      uniform color shadowcolor = 0;

      uniform float  lightID          = 0;
      uniform string __category       = "";

      output varying float __shadowF = 0;
      output varying color __shadowC = 0;
      output varying color __unshadowed_Cl = 0;
      output float __nondiffuse = 0;  /* set to 1 to exclude from diffuse light */
      output float __nonspecular = 0; /* set to 1 to exclude from highlights */
)
{
  uniform float factor;
  uniform float shadowsize[2];
  if( shadowname != "" ) {
    if ( shadowname == "raytrace" ) factor = 0.2;
    else {
      
      textureinfo( shadowname, "resolution", shadowsize );
      factor = 1/shadowsize[0];
    }
  }

  solar( vector "shader" ( 0, 0, 1 ), 0 ) {
    if( shadowname != "" ) {
      textureinfo( shadowname, "resolution", shadowsize );
      __shadowF = shadow( shadowname, Ps, "samples", shadowsamples, "blur", shadowfiltersize*factor+shadowblur, "bias", shadowbias, "width", 1 );
    } else {
      __shadowF = 0.0;
      __shadowC = lightcolor;
    }

#if defined ( AIR ) || defined ( AQSIS )
    __shadowC = color( mix( comp( lightcolor, 0 ), comp(shadowcolor,0), __shadowF ),
                       mix( comp( lightcolor, 1 ), comp(shadowcolor,1), __shadowF ),
                       mix( comp( lightcolor, 2 ), comp(shadowcolor,2), __shadowF )	);
#else
    __shadowC = mix( lightcolor, shadowcolor, __shadowF );
#endif


    Cl = intensity;
    __unshadowed_Cl = Cl;
    Cl *= __shadowC;
  }

}
