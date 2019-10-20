import three;
import geometry;

real
    xx, xy, xz,
    yx, yy, yz,
    zx, zy, zz;
triple pv;

void set_viewpoint(real alpha, real beta, real d, triple v=(0,0,0)) {
    xx = + cos(alpha); xy = + sin(alpha) * cos(beta); xz = + sin(alpha) * sin(beta);
    yx = - sin(alpha); yy = + cos(alpha) * cos(beta); yz = + cos(alpha) * sin(beta);
    zx = 0; zy = + sin(beta); zz = - cos(beta);
    pv = v + d * ( - sin(alpha) * sin(beta), - cos(alpha) * sin(beta), + cos(beta));
}

// preserve vertical lines
void set_viewpoint_v(real alpha, real beta, real d, triple v=(0,0,0)) {
    xx = + cos(alpha); xy = 0; xz = + sin(alpha);
    yx = - sin(alpha); yy = 0; yz = + cos(alpha);
    zx = 0; zy = 1; zz = 0;
    pv = v + d * ( - sin(alpha) * sin(beta), - cos(alpha) * sin(beta), + cos(beta));
}

pair P(triple p) {
    real x = p.x - pv.x, y = p.y - pv.y, z = p.z - pv.z;
    return (
        xx * x + yx * y + zx * z ,
        xy * x + yy * y + zy * z ) /
      ( xz * x + yz * y + zz * z );
}

pen sdashed = linetype(new real[] {4, 4});

pen mainline = linewidth(1);
pen altline = defaultpen;
pen maindashed = mainline+sdashed;
pen altdashed = altline+dashed;
pen facefill = opacity(1/3)+gray(2/3);
pen spherefill = opacity(2/3)+gray(2/3);
void edot(Label L, point pX, align align, pen p=defaultpen)
    { dot(L, pX, align, p, Fill(white)); }
void edot(point pX, pen p=defaultpen)
    { dot(pX, p, Fill(white)); }
pen anglefill = opacity(2/3)+gray(2/3);

void hidedraw( triple pA, triple pB, triple pC, triple pD,
    pen p1=altline, pen p2=altdashed
) {
    pair p2X = extension(P(pA), P(pB), P(pC), P(pD));
    draw(P(pA)--p2X, p1);
    draw(p2X--P(pB), p2);
}

void marksphere( triple pC, real r,
    pen fillpen=spherefill
) {
    real
        d = abs(pv - pC),
        b = sqrt(d**2 - r**2),
        h = r * (b/d),
        u = r * (r/d), v = d - u;
    triple pX = (pv * u + pC * v) / d;
    fill((path)conic(
        P(pX + h * unit(cross(pv - pC, (1,0,0)))),
        P(pX + h * unit(cross(pv - pC, (1,1,0)))),
        P(pX + h * unit(cross(pv - pC, (1,2,0)))),
        P(pX + h * unit(cross(pv - pC, (1,3,0)))),
        P(pX + h * unit(cross(pv - pC, (1,4,0))))
    ), fillpen);
}

real mr3 = 1.0;
void markangle3( triple pA, triple pB, triple pC,
    pen drawpen=altline, pen fillpen=anglefill
) {
    pA = pB + mr3 * unit(pA - pB);
    pC = pB + mr3 * unit(pC - pB);
    triple pD = pB + mr3 * unit(pA + pC - 2 pB);
    fill(P(pB)--P(pA)..P(pD)..P(pC)--cycle, fillpen);
    draw(P(pA)..P(pD)..P(pC), drawpen);
}
void markrightangle3( triple pA, triple pB, triple pC,
    pen drawpen=altline, pen fillpen=anglefill
) {
    pA = pB + mr3 * unit(pA - pB);
    pC = pB + mr3 * unit(pC - pB);
    triple pD = pA + pC - pB;
    fill(P(pA)--P(pD)--P(pC)--P(pB)--cycle, fillpen);
    draw(path(pA--pD--pC, P=P), drawpen);
}

// size(7cm, 4cm);

// set_viewpoint(1.0, 0.30, 20);

// draw(path(pA--pB, P=P), mainline);
// hidedraw(pA, pB, pC, pD, altline, altdashed);

