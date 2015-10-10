/* hellofortran.f -- translated by f2c (version 20050501).
   You must link the resulting object file with libf2c:
	on Microsoft Windows system, link with libf2c.lib;
	on Linux or Unix systems, link with .../path/to/libf2c.a -lm
	or, if you install libf2c.a in a standard place, with -lf2c -lm
	-- in that order, at the end of the command line, as in
		cc *.o -lf2c -lm
	Source for libf2c is in /netlib/f2c/libf2c.zip, e.g.,

		http://www.netlib.org/f2c/libf2c.zip
*/

#include "f2c.h"

/* Table of constant values */

static integer c__9 = 9;
static integer c__1 = 1;

/* File  hellofortran.f */
/* Subroutine */ integer hellofortran_(n)
integer *n;
{
    /* zz System generated locals */
    integer i__1;

    /* Builtin functions */
    integer s_wsle(), do_lio(), e_wsle();

    /* Local variables */
    static integer i__;

    /* Fortran I/O blocks */
    static cilist io___2 = { 0, 6, 0, 0, 0 };


    i__1 = *n;
    for (i__ = 0; i__ <= i__1; ++i__) {
	s_wsle(&io___2);
	do_lio(&c__9, &c__1, "Fortran says hello", (ftnlen)18);
	e_wsle();
/* L100: */
    }
} /* hellofortran_ */

