surface sttexture (string texturename = "") {

/* for all the others */
//uniform string tn = concat (texturename, ".tif");

#ifdef PRMAN
  /* prman  */  uniform string tn = concat (texturename, ".tex");  /**/
#endif

#ifdef AIR
  /* air  */  uniform string tn = concat (texturename, ".tx");  /**/
#endif

#ifdef BMRT
  /* BMRT 2.6 and later  */  uniform string tn = concat (texturename, ".tex");  /**/
#endif

#ifdef RDC
  /* RDC 3.1.X and later  */  uniform string tn = concat (texturename, ".map");  /**/
#endif

#ifdef AQSIS
   uniform string tn = concat (texturename, ".teq");
#endif

#ifdef DELIGHT
    uniform string tn = concat (texturename, ".tdl"); 
#endif

#ifdef ENTROPY
    uniform string tn =concat (texturename, ".tif");
#endif

#ifdef PIXIE
    uniform string tn =concat (texturename, ".tif");
#endif

/* This is the common code for all renderers, I suppose */

Ci = (texturename != "") ? color texture(tn,s,t) : color(1,1,1);

}
