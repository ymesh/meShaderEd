/*
**
** The contents of this file are subject to the Mozilla Public License Version 1.1 (the
** "License"); you may not use this file except in compliance with the License. You may
** obtain a copy of the License at http://www.mozilla.org/MPL/
**
** Software distributed under the License is distributed on an "AS IS" basis, WITHOUT
** WARRANTY OF ANY KIND, either express or implied. See the License for the specific
** language governing rights and limitations under the License.
**
** The Original Code is the Liquid Rendering Toolkit.
**
** The Initial Developer of the Original Code is Colin Doncaster. Portions created by
** Colin Doncaster are Copyright (C) 2002. All Rights Reserved.
**
** Contributor(s): Moritz Moeller
**
**
** The RenderMan (R) Interface Procedures and Protocol are:
** Copyright 1988, 1989, Pixar
** All Rights Reserved
**
**
** RenderMan (R) is a registered trademark of Pixar
**
*/

/* ______________________________________________________________________
**
** liquidtools.h Source
** ______________________________________________________________________
*/

string liqPass() {
  uniform string pass = "unknown";
  option( "user:pass", pass );
  return pass;
}

float liqReceivesShadows() {
  uniform float receive = 1;
  attribute( "user:receivesshadows", receive );
  return clamp( receive, 0, 1 );
}

string liqSelfSubset() {
  uniform string subset = "";
  attribute( "identifier:name", subset );
  return subset;
}

// Returns the adjusted number of samples based on the global user settings
float liqGlobalRayTraceSamples( uniform float samples ) {
  uniform float usersamples;

  uniform float breadthscale;
  if( option( "user:tracebreadthfactor", breadthscale ) == 1 ) 
    usersamples = ceil( samples * breadthscale );
  else 
    usersamples = samples;
  
  uniform float depthscale;
  if( ( option( "user:tracedepthfactor", depthscale ) == 1 ) && ( depthscale > 1 ) ) 
  {
    uniform float raydepth;
    uniform float factor = 0.5;
    rayinfo( "depth", raydepth );
    if( raydepth > 0 ) 
    {
      depthscale = pow( factor, raydepth );
      usersamples = ceil( factor * depthscale );
    }
  }
  
  return usersamples;
}


#define LIQ_BAKE_INIT                                                         \
  float _liqBakePass = liqGetPass() == "bake";                                \
  string _liqObjectName = "";                                                 \
  attribute( "identifier:name", _liqObjName )


#define LIQ_BAKE_OR_LOOKUP( bakename, s, t, func, dest ) {                    \
  if( _liqBakePass != 0 ) {                                                   \
  dest = func( s,t );                                                       \
  string bakefilename = concat( objname, ".", bakename, ".bake" );          \
  bake( bakefilename, s, t, dest );                                         \
  } else {                                                                    \
  string filename = concat( objname, ".", bakename, ".tx" );                \
  dest = texture( filename, s, t );                                         \
  }                                                                           \
}


#define LIQ_BAKE( bakename, s, t, dest ) {                                    \
  if( _liqBakePass != 0 ) {                                                   \
  string bakefilename = concat( objname, ".", bakename, ".bake" );          \
  bake( bakefilename, s, t, dest );                                         \
  }                                                                           \
}


float liqCalculateEnvSampleArea(
    float hemisphere;
    float numSamples;
    )
{
    return 0.5 * (hemisphere / numSamples);
}

void liqBuildEnvironmentVectors(
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