#ifndef ME_ENV_H
#define ME_ENV_H
#include "raysphere.h"
/*
 Based on code from reflections.h (c) Copyright 1990-2001 Exluna, Inc. and Larry Gritz.
 ....
 "In ordinary circumstances, we just do environment mapping, assuming
 that the environment map was formed in the named coordinate system
 given by envspace.  If envrad != 0, we do "fake ray tracing" against
 a sphere of that radius, in order to simulate parallax..." sad Larry Gritz.
 
 */
vector meRayEnvSphere( 
      point Q;
      uniform string envspace;
      varying vector R;
      uniform float envrad;
)
{
  vector Rsp = R;
  if ( envspace != ""  )
  {
    Rsp = normalize (vtransform (envspace, R));
    if ( envrad != 0 ) 
    {
      /* Transform to the space of the environment map */
      point Psp = transform (envspace, Q);
      uniform float r2 = envrad * envrad;
      /* Clamp the position to be *inside* the environment sphere */
      if ((vector Psp).(vector Psp) > r2)
        Psp = point (envrad * normalize (vector Psp));
      float t0, t1;
      float intersect_number = raysphere (Psp, Rsp, envrad, 1.0e-4, t0, t1);
      if (  intersect_number > 0 )
        Rsp = vector (Psp + t0 * Rsp);
    }
  }
  return Rsp;
}

#endif 	    
