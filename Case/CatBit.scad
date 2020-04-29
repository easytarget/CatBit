// CatBit case
$fn=90; // or it's fugly
include<./threads.scad>; // threads library for screwbase

screwmount=true;  // Enabling this slows rendering.. use for final model

// Below dimensions include fitting allowance..
bitz=2; // microbit pcb thickness
bitx=52; // microbit pcb wide
bity=42.4; // microbit pcb high
headz=2.8; // LED unit base thickness
headxy=46; // LED unit x/y dimenstion
base=1.5; // Base thickness
lid=1.5; // the lid, with slots for led unit
sw=37.8; // Spacing betwween screws for lid/cam unit

difference() {
  box();
  // cables at rear
  translate([0,-headxy/2,base+bity-1])
  minkowski() {
    cube([30,6,base*2],center=true);
    sphere(0.5);
  }
  // USB socket on microbit
  translate([0,headxy/2+1,0])
  minkowski() {
    cube([10,8,base*3],center=true);
    sphere(0.5);
  }
  // microbit opening
  translate([0,headxy/2+1,base+bity/2+1])
  cube([bitx-1,bitz+4,bity+2],center=true);
  // microbit pcb
  translate([0,headxy/2+1,base+bity/2+1])
  cube([bitx+1,bitz,bity+2],center=true);
  // Screwthread for mounting
  if (screwmount) {
    translate([0,0,-1])
    scale([1.06,1.06,1]) // scale x and y for fit
    english_thread (diameter=1/4, threads_per_inch=20, length=0.4);
  } else {
    translate([0,0,-1])
    cylinder(d=6,h=10);
  }
  // Lid/led unit screw holes
  translate([-sw/2,-sw/2+3,base+bity-6]) cylinder(d=3.3,h=9,$fn=6);
  translate([sw/2,-sw/2+3,base+bity-6]) cylinder(d=3.3,h=9,$fn=6);
}

  // lid
translate([0,80,lid]) {
  linear_extrude(2,convexity=4) difference() {
    outline();
    translate([0,-1]) minkowski() {
      square([bitx+1,headxy-1],center=true);
      circle(0.5);
    }
  }
}
translate([0,80,0]) {
  linear_extrude(lid,convexity=4) difference() {
    outline();
    translate([-sw/2,-sw/2+3]) circle(d=4);
    translate([sw/2,-sw/2+3]) circle(d=4);
  }
}

module box() {
  // base
  linear_extrude(base,convexity=4) outline();
  // walls
  translate([0,0,base]) 
  linear_extrude(bity,convexity=4) difference() {
    outline();
    translate([0,-1]) minkowski() {
      square([bitx+1,headxy-1],center=true);
      circle(0.5);
    }

  }
  // screwmount boss
  translate([0,0,base])
  cylinder(d1=16,d2=10,h=6);
  // lid screws
  hull() {
    translate([-sw/2,-sw/2+3,base+bity-6]) cylinder(d=7,h=7.9);
    translate([-bitx/2,-headxy/2,base+bity/2-1]) cube([2,2,bity-2],center=true);
  }
  hull() {
    translate([sw/2,-sw/2+3,base+bity-6]) cylinder(d=7,h=7.9);
    translate([bitx/2,-headxy/2,base+bity/2-1]) cube([2,2,bity-2],center=true);
  }
}

module outline() {
  minkowski() {
    square([bitx,headxy],center=true);
    circle(r=3);
  }
}