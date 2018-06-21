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
** liquidchecker.sl Source
**
** Some fancy procedural "checkerboard" to put behind shader previews
** ______________________________________________________________________
*/

surface liquidchecker( float frequency = 4.5; float mode = 0; ) {
  if ( mode == 0 ) {
    color a = 0.33;
    color b = 0.66;
    varying float ss, tt, x, y;

    ss = s * frequency;
    tt = t * frequency;
    x = mod( ss - 0.5, 1 );
    y = mod( tt - 0.5, 1 );

    x = filterstep( 0.5, x, x + du );
    y = filterstep( 0.5, y, y + du );

    Oi = Os;
    Ci = Os * mix(mix( a * x, ( b - x ), y ), color(0.85), 0.8);
  }
  if ( mode == 1 ) {
    Oi = Os;
    Ci = Os * 0.5;
  }
}





