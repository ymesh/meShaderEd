/*
    Empty shader with all kind of args to test liquid sl parsing capabilities
*/
surface empty (  
    	float basicFloat    	=   0.123;
		float arrayFloat[3] 	=   { 0.5, 1.5, 3.0 };
		color basicColor    	=   color( 0.5, 0.6, 0.8 ); 
		color arrayColor[2] 	=   {
		    	    	    	    	color( 0.4, 0.2,  0.6 ),
		    	    	    	    	color( 1, 2.0, 3 )
		    	    	    	    };
		point basicPoint    	=   point( 7.1, 7.2, 7.3 );
		point arrayPoint[3]     =   {
		    	    	    		point( 1.1, 1.2, 1.3 ),
		    	    	    		point( 2.1, 2.2, 2.3 ),
		    	    	    		point( 3.1, 3.2, 3.3 )
		    	    	    	    };
		vector basicVector    	=   vector( 8.1, 8.2, 8.3 );
		vector arrayVector[3]   =   {
		    	    	    		vector( 0.1, 0.2, 0.3 ),
		    	    	    		vector( 2.1, 2.2, 2.3 ),
		    	    	    		vector( 4.1, 4.2, 4.3 )
		    	    	    	    };
		normal basicNormal    	=   normal( 11.1, 11.2, 11.3 );
		normal arrayNormal[3]   =   {
		    	    	    		normal( 21.1, 21.2, 21.3 ),
		    	    	    		normal( 22.1, 22.2, 22.3 ),
		    	    	    		normal( 23.1, 23.2, 23.3 )
		    	    	    	    };
		string basicString    	=   "thisisatest";
		string arrayString[4]   =   {
		    	    	    		"this",
		    	    	    		"is",
		    	    	    		"a",
									"test"
		    	    	    	    };
		matrix basicMatrix  	= matrix(   1.1, 2.5, 3.9, 4.03,
		    	    	    	    	    5.2, 6.6, 7.0, 8.04,
						  					9.3, 10.7, 11.01, 12.05,
										    13.4, 14.8, 15.02, 16.06 );
		matrix arrayMatrix[2]  	=   {
		    	    	    	    	matrix(     31.1, 32.5, 33.9, 34.3,
		    	    	    	    			    35.2, 36.6, 37.0, 38.04,
												    39.3, 40.7, 41.01, 42.05,
							 						43.4, 44.8, 45.02, 46.06 ),
		    	    	    	    	matrix(     11.1, 12.5, 13.9, 14.03,
			    	    	    	    		    15.2, 16.6, 17.0, 18.04,
												    19.3, 20.7, 21.01, 22.05,
												    23.4, 24.8, 25.02, 26.06 )
       	    	    	    	    };							
)
{
    Ci = 1;
}
