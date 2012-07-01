/* Shading models using in Blender.

   This is a part of RIBKit project (http://ribkit.sourceforge.net).

   Author: Konstantin Evdokimenko aka Qew[erty] (qewerty@gmail.com).
             
   License: GNU GPL version 2.
   
   Comment: For details look into blender sources
            (.../source/blender/render/intern/source/shadeoutput.c).
*/

#define color2float(col) ((comp(col, 0) + comp(col, 1) + comp(col, 2)) / 3)

// for toon BEGIN
#define blend(a,b,x) ((a) * (1 - (x)) + (b) * (x))
#define union(a,b)        ((a) + (b) - (a) * (b))

float
toonspec(vector N, V; float roughness)
{
  float C = 0;
  vector H;

  illuminance(P, N, PI/2) {
    H = normalize(normalize(L)+V);
    C += pow(N.H, 1/roughness);
  }
  return C;
}
// for toon END

float saacos(float fac)
{
	float result;
	
	if(fac <= -1.0) 
		result = PI;
	else if(fac >= 1.0)
		result = 0.0;
	else
		result = acos(fac);
	
	return result;
}

float sasqrt(float fac)
{
	float result;
	
	if(fac <= -1.0) 
		result = 1;
	else if(fac >= 1.0)
		result = 0.0;
	else
		result = sqrt(fac);
	
	return result;
}

float minnaert_diff(float nl; normal n; vector v; uniform float darkness)
{
	float result, nv;

	/* nl = dot product between surface normal and light vector */
	if(nl <= 0.0)
	{
		result = 0.0;
	}
	else
	{
		/* nv = dot product between surface normal and view vector */
		nv = n . v;
		if (nv < 0.0)
			nv = 0.0;

		if (darkness <= 1.0)
			result = nl * pow(max(nv * nl, 0.1), (darkness - 1.0)); /* The Real model */
		else
			result = nl * pow((1.001 - nv), (darkness  - 1.0)); /* Nvidia model */
	}
	
	return result;
}

/* mix of 'real' fresnel and allowing control. grad defines blending gradient */
/* float fresnel_fac(vector view; vector vn; float grad; float fac)
{
	float result; 
	float t1, t2;
	
	if(fac == 0)
	{
		result = 1;
	}
	else
	{
		t1 = view . vn;
		if(t1 > 0)  t2 = 1 + t1;
		else t2 = 1 - t1;
		
		t2 = grad + (1-grad) * pow(t2, fac);
		
		if(t2 < 0) t2 = 0;
		else if(t2 > 1) t2 = 1;
		
		result = t2;
	}
	
	return result;
}

float fresnel_diff_1(normal vn; vector lv; float fac_i; float fac)
{
	return fresnel_fac(lv, vn, fac_i, fac);
} */

/* fresnel_diff is not correct */
float fresnel_diff(normal vn; vector lv; float fac_i; float fac)
{
	float result;
	
	if(fac == 0)
	{
		result = 1;
	}
	else
	{
	
		float Kr, Kt;
		fresnel(lv, vn, (lv.vn < 0 ? 1/fac : fac), Kr, Kt);
		
		result = Kr;
		
		if(result < 0)
			result = 0;
		else if(result > 1)
			result = 1;
	}
	
	return result;
}

/* cartoon render diffuse */
float toon_diff(float nl; float size; float smooth)
{
	float result;
	float ang = saacos(nl);

	if(ang < size) result = 1.0;
	else if(ang >= (size + smooth) || smooth == 0.0) result = 0.0;
	else result = 1.0 - ((ang - size) / smooth);

	return result;
}

/* Oren Nayar diffuse */
float orennayar_diff(float nl; normal n; vector l; vector v; float rough)
{
	float i, nh, nv, vh, realnl;
	vector h;
	float a, b, t, A, B;
	float Lit_A, View_A;
	vector Lit_B, View_B;
	
	float result;
	
	h = v + l;
	h = normalize(h);
	
	nh = n . h; /* Dot product between surface normal and half-way vector */
	if(nh < 0.0) nh = 0.0;
	
	nv = n . v; /* Dot product between surface normal and view vector */
	if(nv <= 0.0) nv= 0.0;
	
	realnl= n . l; /* Dot product between surface normal and light vector */
	if(realnl <=0.0) result = 0.0;
	else
	{
		
	if(nl < 0.0) result = 0.0;
	else
	{
	
	vh= v . h; /* Dot product between view vector and halfway vector */
	if(vh <= 0.0) vh= 0.0;
	
	Lit_A = saacos(realnl);
	View_A = saacos(nv);
	
	Lit_B = l - realnl*n;
	Lit_B = normalize(Lit_B);
	
	View_B = v - nv*n;
	View_B = normalize(View_B);
	
	t = Lit_B . View_B;
	if( t < 0 ) t = 0;
	
	if( Lit_A > View_A ) {
		a = Lit_A;
		b = View_A;
	}
	else {
		a = View_A;
		b = Lit_A;
	}
	
	A = 1.0 - (0.5 * ((rough * rough) / ((rough * rough) + 0.33)));
	B = 0.45 * ((rough * rough) / ((rough * rough) + 0.09));
	
	b *= 0.95;	/* prevent tangens from shooting to inf, 'nl' can be not a dot product here. */
				/* overflow only happens with extreme size area light, and higher roughness */
	i = nl * (A + (B * t * sin(a) * tan(b)));
	
	result = i;
	
	}
	}
	
	return result;
}

color blender_diffuse(string model;
                      normal Nn; vector v;
                      float fac_i; float fac; 
                      float rough; uniform float darkness;
                      float size; float smooth)
{
	extern point P;
	
	color result = 0;
	
	illuminance(P, Nn, PI/2)
	{
		vector Ln = normalize(L);
		
		float inp = Ln . Nn;
		color diff = inp;
		
		if(model == "Fresnel")
			result += Cl; //fresnel_diff(Nn, v, fac_i, fac) * Cl;
		else if (model == "Minnaert")
			result += minnaert_diff(inp, Nn, v, darkness) * Cl;
		else if (model == "Toon")
			result += toon_diff(inp, size, smooth) * Cl;
		else if (model == "Oren-Nayar")
			result += orennayar_diff(inp, Nn, Ln, v, rough) * Cl;
		else
			result += diff * Cl;
	}
	
	if(model == "Fresnel")
		result *= fresnel_diff(Nn, v, fac_i, fac);
	
	return result;
}

float spec(float inp; float hard)	
{
	float b1;
	float result;
	
	if(inp >= 1.0) result = 1.0;
	else if (inp <= 0.0) result = 0.0;
	else
	{
	
	b1= inp*inp;
	/* if(b1 < 0.01) b1 = 0.01;	
	
	if((hard & 1) == 0)  inp= 1.0;
	if(hard & 2)  inp *= b1;
	b1*= b1;
	if(hard & 4)  inp *= b1;
	b1*= b1;
	if(hard & 8)  inp *= b1;
	b1*= b1;
	if(hard & 16) inp *= b1;
	
	b1 *= b1;

	if(b1<0.001) b1= 0.0;	

	if(hard & 32) inp*= b1;
	b1*= b1;
	if(hard & 64) inp*=b1;
	b1*= b1;
	if(hard & 128) inp*=b1; */

	if(b1<0.001) b1= 0.0;	

	/* if(hard & 256) {
		b1*= b1;
		inp*=b1;
	} */
	result = inp;
	}

	return result;
}

/* reduced cook torrance spec (for off-specular peak) */
float cooktorr_spec(normal n; vector l; vector v; float hard; float tangent)
{
	float i, nh, nv;
	vector h;
	
	float result;

	h = v + l;
	h = normalize(h);

	nh = n . h;
	if(tangent != 0) nh = sasqrt(1.0 - nh*nh);
	else if(nh < 0.0) result = 0.0;
	else
	{
	
	nv= n . v;
	if(tangent != 0) nv = sasqrt(1.0 - nv*nv);
	else if(nv < 0.0) nv= 0.0;

	i= spec(nh, hard);

	i= i/(0.1+nv);
	result = i;
	}
	
	return result;
}

/* Blinn spec */
float blinn_spec(normal n; vector l; vector v; float refrac; float sp; float tangent)
{
	float i, nh, nv, nl, vh;
	vector h;
	float a, b, c, g, p, f, ang;
	g = 0;
	
	float spec_power = sp;
	
	float result;

	if(refrac < 1.0) result = 0.0;
	else
	{
	if(spec_power == 0.0) result = 0.0;
	else
	{
	
	/* conversion from 'hardness' (1-255) to 'spec_power' (50 maps at 0.1) */
	if(spec_power < 100.0)
		spec_power = sqrt(1.0 / spec_power);
	else spec_power = 10.0 / spec_power;
	
	h = v + l;
	h = normalize(h);

	nh = n . h; /* Dot product between surface normal and half-way vector */
	if(tangent != 0) nh = sasqrt(1.0 - nh*nh);
	else if(nh < 0.0) result = 0.0;
	else
	{

	nv = n . v; /* Dot product between surface normal and view vector */
	if(tangent != 0) nv = sasqrt(1.0 - nv*nv);
	if(nv<=0.01) nv = 0.01;				/* hrms... */

	nl= n . l; /* Dot product between surface normal and light vector */
	if(tangent != 0) nl = sasqrt(1.0 - nl*nl);
	if(nl <= 0.01) {
		result = 0.0;
	}
	else
	{

	vh= v . h; /* Dot product between view vector and half-way vector */
	if(vh <= 0.0) vh = 0.01;

	a = 1.0;
	b = (2.0*nh*nv)/vh;
	c = (2.0*nh*nl)/vh;

	if( a < b && a < c ) g = a;
	else if( b < a && b < c ) g = b;
	else if( c < a && c < b ) g = c;

	p = sqrt((refrac * refrac)+(vh*vh)-1.0);
	f = (((p-vh)*(p-vh))/((p+vh)*(p+vh)))*(1+((((vh*(p+vh))-1.0)*((vh*(p+vh))-1.0))/(((vh*(p-vh))+1.0)*((vh*(p-vh))+1.0))));
	ang = saacos(nh);

	i= f  * g * exp((-(ang*ang) / (2.0*spec_power*spec_power)));
	if(i < 0.0) i= 0.0;
	
	result = i;
	}
	}
	}
	}
	
	return result;
}

float phong_spec(normal n; vector l; vector v; float hard; float tangent)
{
	vector h;
	float rslt;
	
	h = l + v;
	h = normalize(h);
	
	rslt = h . n;
	if(tangent != 0) rslt = sasqrt(1.0 - rslt*rslt);
		
	if(rslt > 0.0) rslt = spec(rslt, hard);
	else rslt = 0.0;
	
	return rslt;
}

/* cartoon render spec */
float toon_spec(normal n; vector l; vector v; float size; float smooth; float tangent)
{
	vector h;
	float ang;
	float rslt;
	
	h = l + v;
	h = normalize(h);
	
	rslt = h . n;
	if(tangent != 0) rslt = sasqrt(1.0 - rslt*rslt);
	
	ang = saacos(rslt); 
	
	if(ang < size) rslt = 1.0;
	else if(ang >= (size + smooth) || smooth == 0.0) rslt = 0.0;
	else rslt = 1.0 - ((ang - size) / smooth);
	
	return rslt;
}

/* Ward isotropic gaussian spec */
float wardiso_spec(normal n; vector l; vector v; float rms; float tangent)
{
	float i, nh, nv, nl, angle, alpha;
	vector h;

	/* half-way vector */
	h = l + v;
	h = normalize(h);

	nh = n . h; /* Dot product between surface normal and half-way vector */
	if(tangent != 0) nh = sasqrt(1.0 - nh*nh);
	if(nh<=0.0) nh = 0.001;
	
	nv = n . v; /* Dot product between surface normal and view vector */
	if(tangent != 0) nv = sasqrt(1.0 - nv*nv);
	if(nv<=0.0) nv = 0.001;

	nl = n . l; /* Dot product between surface normal and light vector */
	if(tangent != 0) nl = sasqrt(1.0 - nl*nl);
	if(nl<=0.0) nl = 0.001;

	angle = tan(saacos(nh));
	alpha = max(rms, 0.001);

	i= nl * (1.0/(4.0*PI*alpha*alpha)) * (exp( -(angle*angle)/(alpha*alpha))/(sqrt(nv*nl)));

	return i;
}

color blender_specular(string model;
                       normal Nn; vector V;
                       float hard; float tangent; 
                       float size; float smooth;
                       float refrac; float spec_power; float rms)
{
	extern point P;
	
	color result = 0;
	
	illuminance(P, Nn, PI/2)
	{
		vector Ln = normalize(L);
		
		if(model == "WardIso")
			result += Cl * wardiso_spec(Nn, Ln, V, rms, tangent) ;
		else if (model == "Toon")
			result += Cl * toon_spec(Nn, Ln, V, size, smooth, tangent);
		else if (model == "Phong")
			result += Cl * phong_spec(Nn, Ln, V, hard, tangent);
		else if (model == "Blinn")
			result += Cl * blinn_spec(Nn, Ln, V, refrac, spec_power, tangent);
		else if (model == "CookTorr")
			result += Cl * cooktorr_spec(Nn, Ln, V, hard, tangent);
	}
	
	return result;
}
