"""Python port of destbreso v7.38_finance7 / yhay81 ShopForge v7 tapes."""
from __future__ import annotations

_PAYLOAD = (
    "c-qZfS(5BHj=V}(f6oUAa1qZkHut~AybNsw;ST97V>VXSS=E^eia}8X;BYwp`#<@UKk3&$`BQ#=>VN+0=U3_b+x%(2er_NA^|Sx_Sw2~gKd_(m=d<$jul$i;"
    "W3_YO{V(VL$@d-4Km6P(n@?OL=Ji(P{`mJ3@@tai{zLU2@6%1p2gmm}-B0cqq<`?|%KYc!zWXGm$$`(!*YtgE!z~G$=JECGbZL%nr_;oa$(nobe_@~VGdu1*"
    "$nDH6%;$PA&2;R*W17c*-`9VCe_UCn`|sD!lN{5SI*l;!c73?}{+n&OlHGm0xcmH@1nz!cvrRwK>$|HPGr7Aba`*Y?_WH{4`pN{Z{8@_{9VWl7sn@smKkIbO"
    "{K^(G&arhfxThJagEu=*zdNtncX4k1Wz6lm?tGK_uVpn4|JPskSK<7<9@mTe5;Bc&Utf;v_un7W7}E#JasxRgp3L`iXPvofJ_hX0y{~E0mAR6O(sZ{JUNc@?"
    "Q~uF7|7t$^|7@J}hu8c(%>9+yw+*xMKl7~iwIXln_oC(acQ5F73(4|c#qTn?W`OrSJY39cfX?!1O7lUQm#=spQyLFciFqu3O2v&-{FMAi^X+6h4d!<^CqE~3"
    ")8G7@=Am+8>onhXb1P0(Xc}lg(~9|8I^VN>|GfK+$Eb%B=~lvi3-?#QW|=rXI$dMD#j&30cFBm<{LL3qAKdQqg=~SnT%G2OUR}2-uXnSpTa)kNw!X&Xbv-YQ"
    "Tr_)S#c%xlVLMeYYVy}Mx4Wm!1Kc|E1{C)z^S#PC((Gc|?=_qa_kQK^z0@s1wp(!eUh0PR-%H3LFx;U2$^;$o{VmpMgIWuAyC-_T%Ja^dj~s=!IGrMK$Ig6I"
    "e@&TPJu|kf2G~5l*;%V+VC*h!)3wdHDB_<V^JXM;qx(F8www_)J{`V~Lf;#0__hPf&dhZ&i(eNf8XO7wGsE-JIxTyS{e|v_9p272w~v%W8vb_Fs~G6j2a`(c"
    "yN9g!HpdfVT4M3XOeao=SvOr@2<wcAI~L{xZF#)&sk6Uyn|r>++3Uo-m+IcF)qrOErnrlcHx!Sj<QhLcb#L?PO6zwKDz)FchjQ<0eQodS@h&q5T#wMNTo_b|"
    "Tx)A!_Dvo+1s8;4_Ibfx!S%}eV>`C^bC~?(9I*GTFq02vKA6e(FVb=>+&13?0Ws=h9gVb}Ig@$3X1iO;{pT<c+cq7Iw^=go%>bvtbZK*E=^&RDGN`yK#e3x*"
    "g&H0*+`r)xJ4{=`A5HrwiXXPQY5K3F#I4B=vl8MFjOEH3G5&eOg_!aE{r`Dv0*rYJ#($5VWp1z{M?m%`aP6tvN2~5@+(273znKrGbDZxNN!JGy3{>z9jt`3m"
    "x06Sn*{5^zICJs<bS58He<IEAE&Idw)BXETPUjm<T;1VDZTrV2h;H99v%C3o%5TSw1o$uN(Kr8x^A7hwXS`gQTht$h+8wZQY>nju$LL^D)f^IIU0|IyqPnT&"
    "6-PgxeeubmT-+cVFplGU5NBsM&fk^E;~BsYozdGd4btb+t~%$b*tC&Op46B&YXd%CA&G^1tDO(VzjW#n5e2Tv`B?!`t0I8q@@ntTqAb-QmU&E{9^Sqw2Hs{P"
    "WN&TVYHV50->-L8VhMq*8`Cx}4tZxGuYH?--S!yahWXV@(S_IZ)W6$CjuFfW<I&<lzQMKie*S;GP9}M6Qg%!C<CXU7+%F(CjDJ5Rj_qTt?q?ytF^2)T4@>!="
    "j{_%i`Ca8P*zm4pHHV;$3mY6lmV>iT2Zzl%%?9VT%(KZ@UY_QUXCcRIo2<otpBZdXmzlyN==@-DS}U)|qS6gImLUE3{+$@H;*PaUf*SwX>A*0@!|==nC61^+"
    "Pd!Sa?xYfTo{kV7<pIfnXkGV6Il@EM8!JOu=9AT10k*J;?HB#VN-{9RnSex$MIoL*nhx<qqRc_|WpcaI=kYvpfwGSGXU!o#Lm<b?yM>=-KaD+IBZ<wpGjGrP"
    "JzlA^(_asSK|=@54z~~V9YoME%L4QS{K>B~-GBYBL0Hgxk^8l34y|^xoW7pj;gcUP`^9Yf(r0Es<+wmx0Fpx|=JXzOzR#y>ed&DJ;)LJV#f0pHDPX3Qgg0cU"
    "Wp3S?o*a$H^EmtDnm4b84V4HIvA&zp%31VPN$O|;J;B<sGuorS<}eHv&wrx|&M0-3WL`UUCrX%sc4^ORY91Xqo<s?w1)CO~mreaM7{uuUCI&5=PwEIs<(iz_"
    "v~0Iq#?V3Uz|XOc`JTc;l-WNWQ5OHoVC++?#2qw`K*;Ti`IbG(aeJH$Iu7$To0E8nP?OBkuk5DlSqi~I2Jn-IGj(Qe2S0#h+N{YFZ1{GFZrL1-OfKZ#AV_YC"
    "ihcv0yM3=R#Y_rd``y?gSbkfXuV*Zf(-l}0_BNUqn2mnDpy|fVst4Z;>{jO!W!bj=z;1q+7Wxv?l$KDZzi??#)RTj3A&)AZMIq}{y+?0spaVJ18D$hj&Vx0Y"
    "9RQQE*d`-6se9iicT0UX#!jdbbJV|&rX8>HzRQ2U`!zS?G1CR}QIyW>wV{YT`2`zK#we}Gl<~%u{7imE0PY;@n+`_}1oKgn-2wcG<s_Y!S?Mx2GN0m?`7jk="
    "m4!?tTPv}CDX_+LeayEK=Ti;8GD<0z(-@Al&9i}S3^7loAB7a|iQ{P;=*i_L1mWX^ELS$8?{Ib5$@Q&qLxye+2Y=JV-Hut1j;4gPO!38Upj6J?Buj=ozZg5R"
    "t2?q;_n{MoIq6Tr{oKdP^c<x>`w~7>KWai~Zwwxt)*v|>cMho_yFGZ`JF(mn7*stO#iyG=u4^I9kP$UJkpPN#QF^j`ApioJCO4v37vzUdZRXp)zbbp`s+@18"
    "e39020TTOvBfPbI4d;F3K@si7^)4SN^On62qVIg%bo)Iin8Inx=vmH5gF>x&?uB`U#)Fb&W$sxgR@BAlVGx1eXY?Ka9NCvz0NR-kckJ+!Yr9VQ_^6t)t9$Vc"
    "?W_9v*Ly|Kj6L+Sd8%pukTkD3%g%R=4Lq1%03PJMlfOXP;nC`RgGA0Dl=d*FT)SVDtB%DcS94xgV}Rq#(vQq}nJ8+J5ZXf=t$w+(0_h=u1iFDUxPpJR(*u;H"
    "bSy=5bA$z(f7uaVxB+%V6GDJ^ct0=p=t}oR$`cP|JbDW4Gt9Q1DJI34!1$-Y@c4U>B|sX`1qzyPCpH_D0Zl@YK?3yA>Z1UESDifu4fC0HUz#25v88FECn%mh"
    "kwL6iuCDyeeYc;1uEVRaxa$}S)6Q-}Mn=;`B&hOgUA-G+Cz{!#u;h*&F%!{D0l~qn<?tYgf?^f#G&WN1BaXj;t9!3``ZIZc{^HHnpd|gt?<kCQT>Y{XhL+QL"
    "iZ`iXsEq(8cBac_aSvs4`&{CQ4))-c?bkwJg2iG3hLzzQEgRO`w&Y!ASEOPm?rG{i34xA0ADEgkig&Pv|Jp)WK|aMJ{wpi^$|ItNnneIx-EudlGua1PiEefE"
    "PdXWH(6rSPnP*{XVq*iq7iW&b>%V$5VEhdlV6Cf<#_LhZvRbjJn7S;`R$*x$3U(VPNjZX8Sd!2I+{s#D^RNs16@Y*HH-0d$`~IsE7Tb-B)3q(oFN+QUw(X$b"
    "w1NcvdPKr&eT1QPXl*hx1G28oJ(>1E{7TVePUok9FE+eYn170Oc+yIQTsU8e0rkT_cD_IxW7y_}JtYhD*J9Xr!`1)xiwXF8`qC|MC?tIRPnFQ~Dt8xxK%<@5"
    "Y=9G$SefU><}&>GlH49il>0Qln$<^&ARd*~07uD+<O71llfcfTB(}7PAkvowOLt@)RzLD$>1l}ZH>mYgT-E=~Tpg51h8Hsg*@dTP>KQ<75+mXj(Dn8#HmHFR"
    "hO`xedRkft^7A^O68NKg8OyuMjYNB>`qI;U#&b0|INX+@I&;CZmq0PAHPF&GrhJ6Zs0JvE6IB8f#(9r<i`ProdKD6r`J?+LUCg|?#A56Ry69yf-5%ShVJyrU"
    "5WmTsg2iHSnQLyJCZHht`gsWt<(2v6!#<G9RB|@2B&NpFL4|owi7lA06cD43J+2pEjK#EA<?EH1>ot5>^|)SxrO%XdZs!*u5k9hc8X&+;i)7k3XU7PW%v2^k"
    "v&5|UEAu$4dE5^A?q7v*YMt#BxUGN&JKM(}^E|G<ZYNPrt{lqGAu{3!X3!*LJO0`3C+i{I4B|bL=<DC)n@l0kmq~0#w8kfSV9$efGb4FAE1`~_&tlKBvJg<c"
    "M!e>jGn>$rGV50?gy6Y;#g*4A2Pp99x7jF+*=7FEG-71&8*!Onyqfo%15;)25G4X9>pU8WF2KT%c=eEnM4c_6`{+`f^GhZnux4}?AD0Xe$|&LvJTAmAD7b89"
    "`TB|Zl<J+UN<c>s-UeF?eC_Oa4e}~8BcB2@u@UzPE|_CqA%1UXE@kmMC=qUiGPenaEE~l)iLWZNO&zQ{1=xS;H5sES{_RL?8Akw;<^?2ulN0r~SmVz2xzeA1"
    "#tS}8)wU!%h2-HlGI-FR1(t!;ZyrG$7(0iz8PcRW%F8LC?k|pZatNYHClpe}gMcVN@>?rCZd^UHB=G{;0o3e?b7gKYnD?#>Ubge(4i2xJA}OT%qbS=)*E6$K"
    "{obaaOcIDO(W+*^=h)a1jCtzi-Kx?gnuL`ac2NaQ86@S8X#k!WTvnl&{Vy*yqkQK!-)DPXR)iC}L?WjHk`gNMydMRRhT>86@>+A9h~c@+yq~%YWdxfGJ+BU2"
    "E}TZU;xAOY8VUXm%+0v0&;!e|5FYT7`dKrd#rq=^>>KfS&II}oYTcor(Lo&1tCkcIPf_u^2h`7<uY0y?{qg|E2lOKpjmLT4Ewu6@j+^!0q(95&(lU+Sx>Z%7"
    "9_AWb`R~|zS=2p5^f2{p_pe~Q602SASaLt1(te9X<-$CT1*MJPUR{T^VQr!b*|<#d8kuSYDMMfLCn)+q$JO|AImP8f0>roG`R1^y8D)@ijwg%&aQ4!pH@Kj{"
    "Lzg-VbdCs<S;|~&cp5m<;-v&!yXuY8<`<bMCZh~Sjq|wEjOFa1k$m`M_wiFToP7)Rkn1jX?*X=tQ0Ov6jHYYvRsTuA*aw0lq}uixxML6kDPL9=1iE8mg?%ki"
    "_?JVmEf2Rdvd|)^|MOA1)|pih0A<hE?p;%-YYo!TpbFPJ3O{4CYxvIa*>ipL$9XN@_1#ECa{GSbdZG>Z5<*pzyML&{&XdF_X<oa}GRYIK8Pl~dKx2YQiNX7d"
    "JPi%7f_`AwZ@Jrd`fONG;jg`pin2xqn%`jgah}|O0ASEX4CW1xPy#`Uj0O#wdjO|n#u<t~{|k3o6C1e`fi*F2HNe*zaVL;?XT_Aaw0H+2^b1CebqwHi&~VsB"
    "yNM>zJvSLUG@UtxC^=lPr8pNG*}29t`<t!UYInufK*?)eDRh3VnZiVgpdP;>m1WqU3bi&cGB<ZQky>vMKo9y9l?KW=vs!f_o}0C>EJhwg0Uw07n|Tux!es8W"
    "SGJBT1L~Kvxliw+0vNIT711{(+r=+PMwK^ACk6aDd7nc<Vn|{Bo~I-0>Tp=`4`F3hBlf$UaZM0Qjs^B9iD1xiJL9^^3xO@On-9loNm9giA4t#6l)|s^P1f1y"
    "N8$L}@-4=w`^NYG*x6`YS-c)?T^97;3XGlE`wq*_fz!c?MARvw8`Q(oSJ1i7UJ&5L_=I3Tlkx7<A8e3H6?0^QZ$SJF0+~WhDrNX7I6{RG?*M<$)-{Sh2HU(M"
    "O7YDcwwz$nvG*(3FNOuE-bqwGv@Ls8CK=}z%o?P%D<zo>ht{A_b0CNV)vh*7nzyGYs_5T56`?VRiO<<*a}Y+Obg{j^y<i4jdmf~y0Q+K_o+82wggJCbO|G%<"
    "wE!QzFnN@RQ>0_NY)>WmL|rG9JyY+aL6>nngjK-tFDUz{48{eiqt4o%44i{pA&x>S_6|e5?6XD*z~0)zzEKRa-@G@tF(?)Qqtix(+YPCwWq<UQ`>PkQ-yj0k"
    "9}0Z+$jnVIrT3Ajq!3^vWzU}YN9mP%@Foh>eW-`^^sL0w^XPY3H1j#$BtVoVLJJZvbP+fsKF*vC6migTsklsLkpz-xGjDf}@r+DzGfbmrK0=|?athUv(JJSa"
    "5^8Y+nzJ6<<^sCd@P19stn9TvFxVR*-kl>4W?DGzkwKxWKdeDpo4M{#83U=Z82#(N2Og?YN0Da_XUAn(Yh9$01iBC7q0DahwI0BYY3_TJhlill8RP2!-Y}v<"
    "2iHO=@IEN|G@mbKdw?ztjiRQ5o=;<m1cu!ph)ct|prT_6IU$*eK{0YFjYHIXAj7brzo|bafQ!@)(W2=6)+AQTg*>Z`XN1AB%qT(u&r_(*P-6$o1tn;N&9v#p"
    "gVnI8JF%w06Tn_*q2XX`*nuh|{t5h1%=Bj(=Uf<3k1h_@1(8SRqr%*c@MD@4?9`h#k`M=7W6A>Bi6DVv)BT(YDO7lh42|XKfYL%n9ETRk-zLkZk&v9j5;4fZ"
    "Ibp4K-Jm}57}7(2+&`K7KC%Q#%GmGn=<sCk<Qwo8GX66y&O=Vm#;^+%Ix<0Tz~djzrwbxq1&dG1kdzWvz-7XuBnETGU3y3GOT(8Lm8=R(c@68YS%@T4@GM0I"
    "s>nmpSUI+^T91qw5zBf5_Df|P(ncyX2Zx{#Y*EN}ARS;942sU{z%G2d=$r}MXK@P&ktW2f1CbLa2nplliWAL1<TUgI8B3b-uB>O69vDIf5#eUQN2eR~(I!A7"
    "O|X0lbro6jZ@@M!{|XK%Qx1el8O$C;S$R+?=A6O=9Vo9;vLO|}Aw+pb9_r>us027AP^(4WNERr`W8>qN0U+|ihp^s=P?pPJ;Pj({FY*=mx|cYh+lZ54C>6?A"
    "e^6o;IILmXF459?_j6-D=6IKaM%;o-!#$efNH4XgXq^qCYru78gu_C?Cj~x;KRfrTfbyWJv5_r*`X5I%fFqks@d|o{SanOLiCuMP$pFuBW5mmV(F4F7YQ+{w"
    "znC1Oz?S9*p@@u~tm`=fNGrYQYcuGI?BZ;@pnWlPh=zLmGA=QzD7x9ud4U3KFq%9UM2QpW-&G4>AbM$HKrkS`rWFxgCr;IuK;lVUHFxrU)bEl(fM2$fTK*{y"
    "HP;0kDF7T1qOJ6T6S73=*_E3rV^uStWZ_@dxM(?(sxQVIhX_oGD@GA;rtVb6p?O9*cqK}oh`Bk9t-SEFkUE;d%1$Oal1EAuw*G3=6)MzV8?$5YB}?8~Y0O8X"
    "Jyb&{9>0Wi5b6+7-JT4RAuX&67wQ{YV~}Wm2yUXv0G=(ZRd0TLrTGJ@WQ6orZsPO>wJG=WsdyBB0Vk@!HYYM(HF8^SC4|yDDIY|HDJAepA>#>18&PpDCUY`a"
    "v=^Z#i5(M4E29Q1!gc`4hFWq=0LsP^4P`kGaG9fz+d+!KckU5Ni2-#il{iKlW74Wse03Pgh?^0Bd}u;?T^>S_PbeEH%&SZkLU}LrI9O6Av2;$`W#tdo^fw)t"
    "UqfwIg3On*Fd@izWaF$L+QP)}G`Elt&ATCkm8%2ZHD&K_IQnX38rP@jgr`ryQCmF&3SGN*iY4~9tS+uHbCqL+JPRum%i?(@kX;3k0@Px}pXnR80bKda$Xr`o"
    "R1cUd<)H|cak)l}punY<2jPJ%%+*H7v0ZclF5(vFER?%bjXo~`&j1%!SS1D^SStm$m5ED%!lg<LD+3-iN^P!dU1OcAOzr+){3Fy7NSW-FKM%dSz|~d{AcKjr"
    "S<;hl3^EL5A%Wa!2IiG9XZw>-f}wgBASWVHI-Di;oqO?%lVX{*Lb?-dVBE$aC8~(dY<!~WT1qX6p^xH+W%WFNR$X&?AGdXoU4^>;ks8>ZoN1t<b|#I~t9Rj("
    "3u4G5gO+>7q`wk#K7@)&@lr=){y3WiiNPFo8XX{{vDS8`#L7T=X1tkn_83WAN-CtZcmS|mPi$ltQN7^YKp?CFc>7jK*bwG3mb;bnK7&79E`$8>O^R0Lm}SP4"
    "fE7!Le;|Y(Yq-8ZJ%}6xFu2SdIz$AX#UlWTL753v?qxh>F)LGGDa1x{Rf<g6fGCT^3USuQo7Y2!XJ3U0U};qEn_$z>%nCxYgfk!fJgZbZG!dl=rJRQxFlh-n"
    "nWMCTuUlf8!w5mzZE>asDti_l-OTGOQHj#J9Ei!^!v-A>ES|yT_?W&CU^!*+Z(*VqB84*F#et;bZ<08nIJn0{4oR=0LbCq@JY=o66>A&Y+-?y1ByvesR#Kuq"
    "=ZE@77s@LZDwRtDu`zWG<dU#~>)l8aYVylFIT4SCw|n3OLv3D}L!Vcg6&rb2#oZqN)8$RB;oIj;2QGl#3s?(1Zm_n0>{Pa~(r|6(44_VU0iw}7ps-Oi$VfOs"
    "Fe5!Ac=kD}Gy8b+Za&<mN?L-BT3JonU^G-9i8jwQo3?nUgu29s>>yc^+hLFo>@YTH&I*L~18FPybsaBqD#P2fjP!Q<13PN~?o<YJisYo0+bgLYjbstvNjvXE"
    "aPlZo9T}DhE||zULJi)G-I{Bfjrtaq$dZh;icP07eqB3acbc6V46NButS757`Sy9yU&|a&oeCJ|_X_3Y8s8qP{zZ4JvM7Ds_`~b&SV*PZI(@AEV#M^)vscG8"
    "ZhB}lhqB`xN9r#eiVx{k)ktYCK0JV!f2Is>a2!nTk1n<+V{e%=G`j8F0Vo=BSH2NR5h&eMNf>h9Lnnt-R&S<;L{wfKYr~cEX36_AodE(2@83}G6rFp~Og+e-"
    "5T)@HTivZx#(aZdrzlN7bxPj#&bfKgTWl*EF-wziQ-~Z5mLMqvIGNQ7E>7v@U)e@prV%@@yqmI+Q-yYif%F|=8Om~*u>skrlrr?)7^`R6Nl^of{5K|l4*PDU"
    "7$=iAdgX=DV*PI_$#bkeeho`8=o1>CLjlN{FhLMdEDpXj5dRu4d}K)LU8VEiI0^&*#ulO+Vu^pp{7g$JN;8X6zd4dZmB_zzo;Epi4m?PvR~M^H1uew6m4B>-"
    "s5As&8v0=g1Oopu10_(C2kT`B8(?GQ@MA^|j*9k&=yQ;0p{yA2u3?>ZY0OfeV$sArp5jl?qkZ;M6YdQFd%*Tyi4PZnW&XrL?iVVjyLLAfJTy`d%8wHyp7HR|"
    "m_pjQ4GL9+AFKkeOvxo%#^1l`%wI2Pw|yFb*m!Zc11PE)ehHM8Q6tKzgsQ)AuL}625|I^1rEp(+dAoAJnjWMtP2!jflTI7NHMCz^2<J*!x!Lycm22$$XOM&+"
    "Z>ES4SM%-*K?+QV6U2{C40Sk5k}zq?fS5>)KgBXx2|vT-$baZp7BeAimB$1;$zNIfatJVLsFjt4V)t#qB_@<WsE|}42c*)<j(h+Gxh^mIZ;qW&!M?281to4b"
    "kt6I5^~n)ZK*eZXvasjoSTyb-!45Q8C0gb^PZO(wJ_Cv3uks0bk*(Mm)gF<=rg7;)CK4eLDfnB&hXHs@D1_uO=N)jg(h^!gECk0MV44>g4l7HjjAdpD(eBt2"
    "&X$n4(xpI9NCd|8bfz2S`?1x{F>u9zA0!pNIS||PJikKZ!b!CL#QyS2#I|)5s!_&8JJN5=I8glZWmgGRKF;XZ@x}8O(ZHG32hjUIzB|nG2KwnEln!@65R~Z7"
    "v3(scmce!gA8!bZ!f}0ZRD@TqL5nj5H}#|cl{28Px`pYh4j~g5SqOlyFZha1Wub5kYJ{Cr%0sX}9@tE*#qwjIAG#0Y0hD7N1;d<BdvwJaJ3^(T=~*R~0W~sZ"
    "jiZ!_G67Tbb85h@kitmQ@_BB9WxqQ^gq4h^IGQJFPKjtiG~yagS|5vN2EJgUw*m>A`y5_6cgC`>@*+9(JL8RLDJ`Ux{a0NpQW46~pxVLNgrQpJK|hcEjZhv("
    "mH_B-p&H=Gknjl=Y_CNTxmZhI$YK;iBW>)tegAOnut9tC6q~(rhf{M4|NXhFvbgmKaZ;4gMXuzCwO8~(d85snjX4FNZBc`nR+C0-$8O7qfu7wLy(0MQliN{s"
    "@P%;Y!CKe7WTF1#I)4mon_&5jH^cFV^9wg8xBcyZZf<26{Xg*kF8`4448Zd7KHbE8@KkuuNalN5wDofq%RB+(;(!4>(G%93``U*e19X+*)&hJ^r->Otz;W;W"
    "FYI$PlR3!kXbWZYhxK#msu?OU_Wu6<xYDwW3ZYxKPeRg&z;lW2zW-*Mu4H!~FYd0OZfL&y3RrCJ%J}Z;#`KUyB6s(_g5F#?USEkrgYu~lPJdm{=#>X_UNgV4"
    "g^Uxl{WC*#@Mg~^|9KrUMa3T8^?H-`{Dl+S*)7NS_j+6}BpTUAxUVnA_51Gu)vhczkYnP>Te0fDULrtOa@RDUNcR^J{yMm3ytt<PqjCP#eDwd>IOz|s$wz_U"
    ";n;<>X4Sq{yx^_|y(K0$Lzed{ewWEL1HA9y;Q|!Sh99Ysc)GY_O5=fQ1S!}l5sIOmQo$k2agi{}Q}S~nm0fmDOvAuVN<3~lU8E68Fr8_IBdG0Y{+91i4<|C?"
    ">K?Oe3gr&n*9;u89M>3caR33eiu>F66?^+a>Vw;TzK|`jm#fpvJIOc~R*s?RYh0X1N3}DHbH8$!ATn200;&yvX^&;XvY)Gv?2LEo9ypffdlj6@Hf|*)z<9qB"
    "NP@sBlD2}_1Gi&1E|sv_LBcB&bintwSPhhs0FLl;&GjnJJEuoU$zuoa&W{ioPBp=KbIzStPg3{zlBpca<kDtD7nrVM!^Z-<6!ihm%YCLZqQ<Ag_fhD3qn&8q"
    "1Z&w_i1eI`UnBVBJYn^|v__)0)?esMsx*7kq&T5%OgPC=Bd=nhS07Bu>2M({zPaquu^19-{1-nv!AV=|j0vONpvT)ys&Sig_4o7j37N#amrBx6;-^V2Lf%k3"
    "o|0?)^who0t1GSFMX1z%?;gs%ul2RPuTxzOdzXJgzXFBUOKdpj4z}1S5LljGuvc)svi{hPEq-CJXJIqXQC@#J+*zXsVDh<Gs<ZikR>e@C{7Bzzci?^!_VoHW"
    ")>OJ(XUcN*KA6u6WU%F1pi-E<0Sg(w#w-Gs<o*qp*rBbZx#B)i{ID(34l~b#<p+~<YlNH*2_VKlZ@3UMzQ6xJk4=CvZ^8KQ(X*UhsRXWv$6m&D@2T5I^TOJ5"
    "!Ci8oQZ{CL%q=YLTs>2^v8HC+C68<t><{+V#%D=PQrCZ6{fR_n{nApx*mv?xI^XC}06iHurth@~7eu#jnc3Zxt4GGT#b;Trx{^Pfcen>S<K@cSqW&<{?tqPB"
    "Yb+l)MpxFwLa()h;?tF|tWYO`u_q#3awz+R{ss$B<@BnJ-8g?&CXZ*}yx)c14#1apGSD*+e5H+a@}vf#$Xh_V1Z>3f!Nfgfxx;XORzTFMP(EdIpG8@!5vk`N"
    "pB_y6iS=4le{1VjW6OH}e!a7XG|HUdv^gOmk<70eIh<i&el=4}K&?oP11`r1Bc{9!&a*ty*PrpJ*U2QWP0DWRe!S8isK?b%Y~+Ff?#Ec&&q97<4g+u>mhwR#"
    "=ju#L0tv-n!@HIhQ64*~AhpN5`Hac)Ttdnlh_`2x0mUiJ@hs$+ZIiXw?=yof>M~P!1f3r&PHW}$SX8<}#}cF;-@g+hR@|}1STqVq;|dR^;h75|IUUTJbaXpz"
    "DegQSF9`I5oTeVF>mDgbc*uHVWhl#hvU)4P7FKCB4*teUGBCrLfE0>3c~2lshj{u#oobZS)y%uo=kYvpfwGSGXQ|ve5Cid_rWD;ylZW{#t&5X>>v_M&E2bQ`"
    "9teYm4xAlMPj+vDLRy&x=n43fM`7=`$hb2&!m3v8bSSHSe6gIqp55V-A20jGZ2Hn?W<ce*Ks@_AbYf2LG3T{9P;Ua0fS5#ip<yOwN=bMVagy)3b!&QZG-ANx"
    "&JOzNo(&aBJx}juv~m`GRi;{)p4N_?(F18<D4AZ5L5m8`DD}mU85g)RU6H8g)-^ScjvP;-gwevH<dAXvY144^MWGT}HX*7}B`zMGmMsO+a;ydL9P60xDJ(>p"
    "{nNPj*(EBToq`-QT45`gWx>je8lyrThk2XLNxVd;NuV6)W;b2WQV15p`vPpJlqO%`TPB${Yx0DY(p<7m)8=Soa=)R9Ro1BJ4^^@9grs@co@ryv7QCKs@pjrq"
    "v4<eY{@1XA#=;%n=dB<l0-dbte4;Gd)*skZ`A-8*fi7eD2<gqwcCQxA7V@alSroEPK!VBGKnHT1Gs;vm8!1kXhe>f+at#ZAbuP&oB&>f>E9{4WLqGa`>aj<z"
    "xusa&3-~o<o!r_?0txiBM~R$kxdzyz8-Ym`kP0&CwKv!|^;CZ_A0^oxz@J!7(rKCXK^kmeMPs|nhpFhShE@n?<gya$mjY`{*T;M-aXuB0gHcMkoW@YrY@<c3"
    "C(h$m7OX-)tOi=4ebU=c2*Sq+S+2Ah##g6t*~#^-aYKe~4hR2A;34L#<?uIot@PNjFSUv@Z$^5yt2?q;p-9S`pM?8q%bb2=yuO4F70S(|P?3=~hFk=zfGW;Y"
    "M{t_{Hb-|*otH>KE|TYOOuR=U`Fx9gvR+%Kwjisv1m%oN1HtlXcE0WVtFouA%K2vQN?GLsB=-MCcxyQt*tRKQruM}D8D7e~W$%NiTpH@)hAqrPG&F+ttp&5S"
    "kfu;;o_k?lq4A((S(&<&u7aX2Mh}As{63@a_*SRG7kvpxCjt#n=i07QK0d0Z?CM_p@?rh1+B6wDV-LM-o@$EPdR$}FwG^BUJeXeq9^}1~zd+jI(dvAIM9v|o"
    "4l$#0?S56RIu@H;&G`d6P$jyda{=N90JTUDil^e{VTB*cCv2k$v`!Zwv|b^q+SzWusp7nZ58Z$NH=>U~0Ai-$t=bRee17>5bIKDBWjuNcKQc~hZwP%Q3!RC|"
    "!5SXR+R0vB`q<yj>P}8OeF>FUg9PZK)kgvTu0~)?!+hqVpWcb8>=IYV1&U`+WLQMWHEJPoEBG{9A3hMyqk#fZo?mS@-9+o-pVl=KsdSh-o*#uJcl1zk2+R}^"
    "9L!pd59vw;WE}=G(1U1``s^E+X9hypiVJ&cl$S$NND_y<wt%?3pQqQ2Mni1`I6;a4sM%9<>BB*YGG?Mw7+BeUEd(Z5EH+?R8O~Ah>Ybp~6jJ=n%$L|`QyCw9"
    "XqYzzLJ2~GYa}s4fR;t=)4TS`%d8M;s8!*tBo&<enLL=rQ)MuOdD6*ngQl&X$UF;66B`=<zBqFfUjNmj0poAbfb4owR$z6N2r1qIOcS(KK5se-6?DQffI9<X"
    "sZvt?oZ5bp6DHs6T%1FcxEZ_HFAODzmhkHEo)#huhz<a@?Vw+xYJG@iv+TPtv<|IJW@bRvwIRCIH7x)0lR2HALKUTfeD$_SA+~c$Xp{wC>5+)?g8P95+8Dz&"
    "FYGB<puZNwz8kLow_i-a*VC77fkPqT<A17zo>#ehDZ0Uxy8Uc`6O~w*=f>tT{Q2UWIR;9^iKv+;7LURXQY={kx}_(c1b)$Thzbo_c56<HOku2=m>8`8n<?2("
    "*t973zvx;d6fb_=wdhPe1E@`6M7#pJ-k!zgjejaj+IKdXQa`T~DuF+`m$AI7+(@*CsxLjwXFOMfgTrkZsxucHb-L;3rOm|p0OxxEJ<+ieOcK?n10M4hua~g("
    "DkLWJNB2#-n0a-H#n=yY(aS)(J+@K9SeP>)ev|p$#Hg=L#t`R9$f+dI+t{)tKdqpdb!9~coldM#!MGla%O$p8!csttLiV^``U#sxC0cb4)+;mDYxuD0alHmh"
    "pDE?s&M!b>eGeMZZwAiDWfJpZ5;F-tDdakT&9H6ngLxd*JZ=Yl_pib@wa)em+*a5U_qLDUcJ!-KZ@!FfKV<#G2xibE<k@j<yPvFwbTeuMkxaI%T{*$CPhdOA"
    "Zcr`Hp8AD=bu%M*IxC@$p3h>>v$7CSwQ``}OkHLZx>9ESiiHq7*RQzpn&kim9{n~Og)zGpDbIe}2yXEkahYJen)jRoQ)TcFB?2ewJQ|2Dz`~Ds^^k`|oh_mJ"
    "=#~q0OC}+(26_PnO9lvK6mbV07h)Kcu=@b$#DdKI=5MdetZmd2tg(^EOvFF)1(VoJY{Y$n3+DUD4<-x(TuPwtp9nWXncD<ImW|?@#8;KsrqVXK!2VOO$rx4f"
    "Z%1OwI0BF~FCgigoT$IWX;}47jOpxaTy&}WrFqR^W}Xdb`Y@H<-A46D2|oiu#0I<XaB=j@f;Zfr%|A;2U6dTqOD_;m-vP@vC!kcoRL{1scNQo=K#{z;dH)v9"
    "uH%c%*O~RoOlF|CVFw#lSF2r?P&Q;8=JX+*>N1ZlD1!%d`BR^=L{0}-+kVnWh!L9l2E(``v&a!hE|o>)pf0_*D+LNj^$n~Q2kR<yT?c7ykrQheU?Uy4X_Keg"
    "RiFyz`qIJ{0xTg)vyAtws{1HwJ(W>a|J71tS%A){6*NdFAJPI*9)fLP<ca3O`rs4gT{ha<gC<1>Ir3TKNYwk+<OU0X!E%iB__t~UjEc?>HK6xKdNc0L!eLJx"
    "5F8*^e~_Hi&%g`0jDgI#y~vf0e`)`>)BJ0ou27)?-!rK@nOv`0Uts-h4cm4PS^;?~UE#PwQOBHkBRo{^HW;^8K5u&A!AQN(1l3^F4}i9Ez=w4jwKkODj;J}e"
    "MhtCCz@`OQ=<v%(u63T~22Q!gvIZ=BY1yiSIXJ?PKevs)fDNYCW_CUa^9RZ*CS1{sQF?OMHyNxUf|VWhz59@*rzl3pnlXrJGT7qLwI9pccH9#YFzyS5#4?Hl"
    "(%n<7uvp!E)r}=@kS_sR+@W;^F}*@99!1q1z)Q?ANddI1Ekxm0VtK<vm`nRsyt+4X<pj`Vd~=idHboacRsOz%{x+cZ5{Ivlzf;%)1pO6<L*EL{(1Y{+tJ=1g"
    "QslBwfQ9+8BTAdw51gHL4ioz)f_<wSFl^D3r$c1}wQsO&_^ch-d_o!*Hq8ivz7Vo0+?fn*oyi1LJRq$9<PK}0=ZsixjF7x+4xNYK6t{>%>`4f%F#%rc6!K(H"
    "1A)u0XoQ|Wq*I#psJ2iW4H2b~bLFdEbETjX<V)Qh=+-wDVE28-5Hcf7Z6=`XM{Y<ldX@Y$DsPwvh`ft1Vz*B?$*O=_fJT`MU>kJi7W}M$z>bN9Fg17u;rQUr"
    "feCpPM0pmKqo*~<Oo%iFlwSb=$?*?)ld?mMhtB)}VF4*?Lun1AFfY4Y{%Hdd8PiT&Un{*)TVbJ?5Tgn{usMh2spATIgTUeYbyyO7N{Nue%R^+7JV;4mdY918"
    "r~$yT<8SiWUuV}F7w4`=XOx?QYy8O5{_p>ESh-zJT@+nvYuGlm8d%tNPrj=zkbscQTG&$)qatxEudcAbV1raDIwKSEq4RXXJBxbub|yDG5FDuZ81SNZs4U3h"
    "WwsaTv?A&e29R~2-TDTKJ@qoF$_ii-Rp4yPUX>}E(SlhIcFtt3?6I)n6lU42e}u?q0J2yzQc8;AeVm0dO7&sR{y;^7v`QD-w|Txs?nJ&FDAo-YsP9j4m|fji"
    "qA5QFduA~NB8t<gl*s<0r%1<U+@4DEi5fR5d!`<YS`Iq~1A_R7BZGFG5g-F_uFg7#44h<W*9{mhGcIQ%r*)q-%AwsB)2$!adWrQu-n{R+A=;}t^`Ld5!tI6x"
    "$g)5BZa*s*<YIL|tL_gqvU=bTiu(getjfcXCqzK_Yu}?D{DTrC8c;ZYBM<G#=g1-ZU1@AYnwg<tY4y{dClT-{AI7EnEFhL^ROQUP-4A)tOw^y4%*}j+Lbc))"
    "3JjxF&MT|(9G!+6z}V#!2ToH=dV6}ARgU%t5_lsJ(K+&9rX>iiL9M7itU+g(xpYriXvGllJIO>mRHcq0Pm8Tl^|aQys0|5pAI3wa+VE>VfE&}?_b3k!L8&vw"
    "*8#j?M92-U1t)Bv7`D3e#cYp3<Ni+S*5LUxmPlaO4FY6~Xd_W{Od%&EGd(57@1${vdJkk6BJo#ElWE8z!N9_^a(X5Cg$ffDAogOb6*F6wG{G^5ksws6r?CU("
    "LT5Cnpu04ubfw69bR;icS+nbsJXf@^IzZ;G3}1Wq*Dgpg)2~w+V@`+EqY;92LFCc-s30G)EnEkAQ$=1+{C^I$*!c|L`Odr=W3OzUAXD{gp(I8!G*);6Vg(sh"
    "SGPz(_HaT3Whj~V5oMZ|x{eD;kToOp#J(60S=9ADvII)X@<#IL@MHmL`E<XMkTjnu-j1A}jbRrkbYz;?fC@jHPZvbK3KpMM@+f4WJ5WTK14vtD>RS46ZJ17J"
    "4MAFivRZD}by$DRLL`}jXDO=jL>`L9;;Wp3!ISONdP|(Y8?01yU^BTwPzbgtF`)<L!xZP{%4#5U0(^{|3EXFK3ki`X#E}7!lhBO~dbU^RH*CNa8T1KuQtd<~"
    "D6D6g5J^^-1ua3T8<Sk!ppP~IB58u<Qz%Wy`e%be$MUb>kTT^!m>R(BL6n6jm=keHGTLgWrmGT=lC*qVPyOl*6)!y_p^_Q6@btaBsrpw)c~WxRG5|zg_z>0`"
    "5lST)44i%x!9~6TU-uFRbQ^IpCg>$Wav@hdM~s)j({_mx;@!`U`Iy5yAVPug1jws{`nBA(d6aJ&Ob!7BGjyH(GIR8Tm@Yxp4*g5qE)TL4TfpxeJNbKA7ti?4"
    "tlU%?z5x=uo-HuIbKK%$1bA8jFo#+(K=M&AWd!C>xHYpRimVn_Af%OEw1ydUMRt9&om5-yT&(_#4%*`;!k~#OMZVT|fdXtWnta8leuBoH=3TV_h7Cn&!!ocR"
    "i^nKT5;=kM4U}pM(e@}vG($hHx-;8Sk<8Q&)BgcBvJ`9VbPx}Y2$3gx!3kL+_3Sj?lvNrrpv2~OLB*o7Kt&is69D_X(|eEU1{UmS9D=bRLw)G;0dg*V9b1t>"
    ">LmQ3T_V$xYiu4VQP@4JQCFx?gKf-?y_YO`Yo#$CjrLI4t$6$r(m|+0M5S*sNQShq1%*)G5Eb;H{1Dtkl>s~(V-wswG&{c1`~ejMLJ}roi@f#bg(sTm1W$v%"
    "fD=_<n-dwYdZ8`15)Xovg}@gPrj)=Zg^VX4ZAA6482NRuXfHxf5<4c8*2xbjuc5fwRw#h7u|z{z&V%WkC*NFHiorL(5lV>>FXC8<W3(}if3>2i4nrBSo<GQk"
    "CM0>~Ar$$9%8SCh%0wZQ_gaaAC3O-@=d@j!{cufx(}DRl)OIDvn4|^k36!bk?c}T=+QP)}G`Elt&ATCkm8(M;=U_MLQ<b=Sl{a4KDFo9ijJ=du^%@{VOYCpi"
    "@)>33>Z$Him|#K{&ntoKDu5KAE*<_%-@pyv%4bIA+I-3-#mtq$)}h8+t`Q?BaOveit0W6^wGnb`7hQmhxWzdO<?d9Y&kMjaz{LfYfYw<k1-F&yGkKH^Ra_}s"
    ")Et&}LrQLqrJ^#m`-Ab1kh+SpB1eB7q9XrvzWNRsOq9)%o_u4FVJHg;<W4g%uZ%g{pM(+&)w=*W5uMNBEU|BXi(i}+E0q-@@V|j^TP#9B>s3i53ryEiYDo-z"
    "6hACzK=i(|5N$YcTL;;NockXMIq%7t1{w~`q>*~H|9f&l44H(>&%~s^5_3KfJrxCvv?hbINl-`FqfVm(gfy0`&XiaQeS^k4&~RjZcpyrSGFEVSq84Wz=(ynA"
    "OxYn&V?!^F=Y}w!vD~ek_Zj@@awTEV=VxV(S!PTLSh1A&2SWI<hU*K|gUCSugUigJLqy<TZ~BH`F$Nb7!f_3Vz=#j1tn!>mPY=qML~KAR(4mZ7gv=R-yTlvK"
    "{KEfPun_>>p-xE>&V2CmtWy0=Z<9%1PjZ}fu*(%cE&9e<Vrq$L4kH9<x5b$ncA*iL2oy?%RAmOsftdU~>~ZnH;u%yF4JdPY8B>cY7N2cF79xd8*-nVePWX3|"
    "IHA6_$3qS|$)iHD{{uW^t+!oN58B+Z5Bel`Ie#Vc|8st*e{`X|W|+3QBx7tKSZH;Qgf;0ENM>|a<AI3rtO3%b#gSmB%`0>0^GZgLl!jH@?eRZd-sBp-ecm*&"
    "0_eSfwb0`RYX`+nRn;mD*LKbTY9<#T8qEU=8%2YxkWhbGRY-=->wWA@0gADOLUahc5}@+XX=x0T&z<MG$Yxe*Y+A@F@L7`EVUQ1O(luz#3WWBK>WbHOyvV5x"
    "Z_~0_gT%|dYxu?YbzSKclax+*YDEIzU7YELC+)lw!O7$0w`ECDwdEC%P?>=Nh-gh4^)0HiuAnTX@0iT3rHoZ>P<CoCux3NCo>ThRJ}+8SnFFeGEuQxx-{czK"
    "VXFQ`gQ;Tj6Eptsy1~?nNVq+jS^dR`>7}QX_%`VqhMn3_cD&<A{e?sEAUotXFg`qx3Jzs(gX3Uwe{``unW*DZhDNu|F91bD?#j2!#C_63^NJ-s*e-p#KC9Ht"
    "-b@XNsJuGXhAZdIlJ{pi0|Xe}zoGUcI=6F~6v3VlrSTM7-Q7qAl5?XSj(C%JMBeqzxp~sDwxJ1Qbs>NBYk&5KE*|oU`l&hPrE+mfH~-2u@-mIsdF2g>g`6r>"
    "rxMb4gk>miF~|YgsFX7F-59H9+DTCZi~Kh#72YUao8n|do6K6z!f3JnH<jc$Rv*8Hr5GdD(%g`P@0xH?l}jK`JkUD6s2Nd0<^k%6?;V8^3xnSQe6D}V{7g$J"
    "N;8X6zc~_y*ze?=!x#|oAQ|y*R+$RAaC0mFSPSv2Z0SeUNBv04>6A#6be(Dg33MUU0tq;OKX&S<Xn%-42Z<KSiUIGMu9+xT@>n!6kEb9Jzb`}hsgLyrfIVP)"
    "jZiueU58H`<bDfMf{=x7aV~^-WW?2j^5X=FXFNPKrjT}S15_|YrJ&1Vv$my-zkk!2zh2M|8-pkj^EC0Xywab4S16T*L0`oyL|c^(VK#4jqEfi8y}VsHU`=C6"
    "q!UJF<*k|dfeK8M^Vo%qAxu{eedQWE{~09V$D1i4#MQj}LXZLlQoz-R?HM`0YvWBp%qsu9X|L*7#T!|thn8P46T((`Ou&=;m9;O20HcOlSy?D{-xgeALJ5Ql"
    "NfmNHDy{6u2T+hJ?*{T_?2HQbNh^@@30sp9?9RG4gNfRNv@TiLb8{>jLVi^CLRN{EdC$|tYM{?RqWDSq_c>d!F{(WxiB03ug-j$uQsPgd)*7_DfW?Z+8Vej9"
    "#~6=K2#!6#G%qk5R+dm1OHl4M@UbVHEg^BGOM#$}2#o3JOgGB+i`zC(;EDl1NO*a3AhzduetSF!C(-&7`^zs8+h9bfMj03FNWU@TK=I3$T_sfcxUJ0*`}co?"
    "WLh6U@B8@fFwd);FEk=b;3s+ca#~ZK;?<0o!8X?(ZwQRSaeZ-AgjcRXi!%i`^`rllGoTM*nGY%@j44nEfUht3icV#ra13gM-9XAius<HyOsq@sW1t_p590xp"
    "V;%*=oKQO@#Th$7rKIUuC6-};+=!4EQJE+cFf~7?#`4{Tbq}ClH=$Cx`@1tlSjl*bqj{p{l!z8YBd(!uZUIf3&iw)swHpE|^7HNP=nL6bd669Yo$*Grlory;"
    "{;RGPsR(7jO<wlIRJz-<F(f!nHUNa!xKIsnWJvgg3bxmxh+M3tFJv(ap^-NB+`fNM+oED{;!^XYc~d)Gw5+nY^$2lNl+i`5<cPIb^g(%}&6|xm1)#%HgPB&)"
    "tm}s+`Jey!UyU>=(*"
)
# yhay81 three-day shop router v7 tapes + six-day budget guard (Apache-2.0),
# plus destbreso L_FINANCE (hire-order chained financing). Python port of the
# native finance7 chassis so it can run on Windows and as a one-file submission.

import base64
import json
import math
import zlib
from typing import Any

ITEMS = (
    "WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG",
    "MILK", "WOOL", "FERTILIZER", "GOOSE", "COW", "SHEEP",
)
PRODUCTS = ITEMS[:9]
CROPS = ITEMS[:5]
SEED_COST = (10, 20, 50, 100, 80)
ANIMAL_COST = (300, 400, 500)
LAND_PRICES = (1000, 2000, 4000)
UNIT_OPS = (
    "PASS", "NORTH", "SOUTH", "EAST", "WEST", "PICKUP", "DROP",
    "PLACE", "PLANT", "WATER", "HARVEST", "FERTILIZE", "DIG",
    "BUILD_COOP", "BUILD_PASTURE", "FEED", "COLLECT_FERTILIZER", "CARE",
)
MARKET_OPS = ("NONE", "HIRE", "BUY_LAND", "BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "SELL")
SHOP_ID = {
    "BAKERY": 0, "BRUNCH_SPOT": 1, "FARMERS_MARKET": 2, "ICE_CREAM_SHOP": 3,
    "PET_CAFE": 4, "PIZZA_SHOP": 5, "SMOOTHIE_SHOP": 6, "YARN_STORE": 7,
}
OP_FEED = 15
OP_FERTILIZE = 11
OP_PLACE = 7
M_HIRE = 1
M_BUY_LAND = 2
M_BUY_SEED = 3
M_BUY_PRODUCT = 4
M_BUY_ANIMAL = 5
M_SELL = 6
WHEAT = 0
FERTILIZER = 8
GOOSE = 9
MAX_UNITS = 40
MAX_ORDERS = 10
K_TURNS = 719
K_ROUTES = 2
SEGMENT = 72
DECISION_STEP = 360
L_FINANCE = 1

_RAW = json.loads(zlib.decompress(base64.b85decode(_PAYLOAD)))
_ENCODED = [_RAW[:K_TURNS], _RAW[K_TURNS:]]


def _decode(encoded: str):
    parts = [int(x) for x in encoded.split()]
    n_units, n_orders = parts[0], parts[1]
    i = 2
    units = []
    for _ in range(n_units):
        units.append((parts[i], parts[i + 1], parts[i + 2]))
        i += 3
    orders = []
    for _ in range(n_orders):
        orders.append((parts[i], parts[i + 1], parts[i + 2]))
        i += 3
    if i != len(parts):
        raise ValueError("trailing tape values")
    return units, orders


_TAPES = [[_decode(s) for s in route] for route in _ENCODED]


def _get(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _fib(n: int) -> int:
    prev, cur = 1, 1
    for _ in range(n):
        prev, cur = cur, prev + cur
    return prev


def _qty(n: int) -> int:
    return n if n > 0 else 1


def _plant_tiles(farm) -> int:
    tiles = _get(farm, "tiles", []) or []
    n = 0
    for row in tiles:
        for cell in row or []:
            if isinstance(cell, dict) and (
                cell.get("kind") == "PLANT" or cell.get("crop")
            ):
                n += 1
    return n


def _select_route(obs, seat: int) -> int:
    shops = list(_get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or [])
    inv = _get(_get(obs, "market", {}) or {}, "inventory", {}) or {}
    farms = list(_get(obs, "farms", []) or [])
    if shops and shops[0] == "BAKERY" and float(inv.get("FERTILIZER", 0) or 0) <= 10232.5:
        return 1
    if shops and shops[0] == "PET_CAFE" and len(farms) > 1 - seat:
        if _plant_tiles(farms[1 - seat]) <= 64.5:
            return 1
    return 0


def _emit_unit(op: int, arg: int, n: int):
    name = UNIT_OPS[op] if 0 <= op < len(UNIT_OPS) else "PASS"
    if name in ("PLANT", "PICKUP", "PLACE"):
        item = ITEMS[arg] if 0 <= arg < len(ITEMS) else ITEMS[0]
        return [name, item] if int(n) == 1 else [name, item, int(n)]
    return [name]


def _emit_order(op: int, item: int, n: int):
    name = MARKET_OPS[op] if 0 <= op < len(MARKET_OPS) else "NONE"
    if name in ("NONE", "PASS"):
        return None
    if name in ("HIRE", "BUY_LAND"):
        return [name]
    item_name = ITEMS[item] if 0 <= item < len(ITEMS) else ITEMS[0]
    return [name, item_name, int(n)]


def _to_action(units, orders):
    farmer = _emit_unit(*units[0]) if units else ["PASS"]
    hands = [_emit_unit(*u) for u in units[1:]]
    market = []
    for order in orders:
        emitted = _emit_order(*order)
        if emitted is not None:
            market.append(emitted)
    return {"farmer": farmer, "hands": hands, "market": market}


def _action_at(route: int, step: int):
    if step < 0 or step >= K_TURNS:
        return ([], [])
    return _TAPES[route][step]


def _requirements(obs, seat: int, start: int, end: int, route: int):
    farms = list(_get(obs, "farms", []) or [])
    farm = farms[seat] if 0 <= seat < len(farms) else {}
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    purchase = 0.0
    item_balance = [0] * len(ITEMS)
    starting = [0] * len(ITEMS)
    hires_by_day = [0] * 6
    quadrants = len(list(_get(farm, "unlocked_quadrants", []) or []))
    for step in range(start, end):
        units, orders = _action_at(route, step)
        for op, arg, n in units:
            q = _qty(n)
            if op == OP_FEED:
                item_balance[WHEAT] -= 1
                starting[WHEAT] = max(starting[WHEAT], -item_balance[WHEAT])
            elif op == OP_FERTILIZE:
                item_balance[FERTILIZER] -= 1
                starting[FERTILIZER] = max(starting[FERTILIZER], -item_balance[FERTILIZER])
            elif op == OP_PLACE and 0 <= arg < len(ITEMS):
                item_balance[arg] -= q
                starting[arg] = max(starting[arg], -item_balance[arg])
        for op, item, n in orders:
            q = _qty(n)
            if op == M_HIRE:
                day = min(5, max(0, (step - start) // 24))
                hires_by_day[day] += 1
            elif op == M_BUY_LAND:
                extra = quadrants - 1
                if 0 <= extra < 3:
                    purchase += LAND_PRICES[extra]
                    quadrants += 1
            elif op == M_BUY_SEED and 0 <= item < len(CROPS):
                purchase += SEED_COST[item] * q
            elif op == M_BUY_PRODUCT and item in (WHEAT, FERTILIZER):
                purchase += int(prices.get(ITEMS[item], 0) or 0) * q
                item_balance[item] += q
            elif op == M_BUY_ANIMAL and GOOSE <= item < len(ITEMS):
                purchase += ANIMAL_COST[item - GOOSE] * q
                item_balance[item] += q
    hires_today = int(_get(farm, "hires_today", 0) or 0)
    for day, count in enumerate(hires_by_day):
        first = hires_today if day == 0 else 0
        for index in range(count):
            purchase += _fib(first + index)
    return purchase, starting


def _owned_in_hands(obs, item: int) -> int:
    private = _get(obs, "private", {}) or {}
    inventories = list(_get(private, "inventories", []) or [])
    total = 0
    name = ITEMS[item]
    for carried in inventories[:MAX_UNITS]:
        total += max(0, int((carried or {}).get(name, 0) or 0))
    return total


def _existing_sale(orders, item: int) -> int:
    total = 0
    for op, it, n in orders:
        if op == M_SELL and it == item and n > 0:
            total += n
    return total


def _add_budget_sale(orders, item: int, quantity: int) -> bool:
    if quantity <= 0:
        return True
    for i, (op, it, n) in enumerate(orders):
        if op == M_SELL and it == item:
            orders[i] = (op, it, n + quantity)
            return True
    if len(orders) >= MAX_ORDERS:
        return False
    orders.append((M_SELL, item, quantity))
    return True


def _budget_guard(obs, seat: int, step: int, route: int, units, orders):
    if step % SEGMENT != 0:
        return units, orders
    orders = list(orders)
    farms = list(_get(obs, "farms", []) or [])
    farm = farms[seat] if 0 <= seat < len(farms) else {}
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    private = _get(obs, "private", {}) or {}
    shed = _get(private, "shed", {}) or {}
    end = min(K_TURNS, step + SEGMENT)
    purchase, starting = _requirements(obs, seat, step, end, route)
    cash = float(_get(farm, "money", 0) or 0)
    for item in range(len(PRODUCTS)):
        sold = min(max(0, int(shed.get(ITEMS[item], 0) or 0)), _existing_sale(orders, item))
        cash += sold * int(prices.get(ITEMS[item], 0) or 0)
    shortfall = purchase - cash
    if shortfall <= 0:
        return units, orders
    candidates = []
    for item in range(len(PRODUCTS)):
        price = int(prices.get(ITEMS[item], 0) or 0)
        if price < 2:
            continue
        protected_shed = max(0, starting[item] - _owned_in_hands(obs, item))
        available = max(
            0,
            int(shed.get(ITEMS[item], 0) or 0) - protected_shed - _existing_sale(orders, item),
        )
        if available > 0:
            candidates.append((item, available, price))
    candidates.sort(key=lambda c: (-c[2], c[0]))
    added = 0
    for item, available, price in candidates:
        if shortfall <= 0:
            break
        needed = int(math.ceil(shortfall / price))
        quantity = min(available, needed)
        if not _add_budget_sale(orders, item, quantity):
            continue
        shortfall -= quantity * price
        added += 1
    if added:
        orders = [o for o in orders if o[0] == M_SELL] + [o for o in orders if o[0] != M_SELL]
    return units, orders


def _finance(action, obs, seat: int):
    market = list(action.get("market") or [])
    if not market or len(market) >= MAX_ORDERS:
        return action
    if not any(o and o[0] == "HIRE" for o in market):
        return action
    farms = list(_get(obs, "farms", []) or [])
    if seat is None or seat < 0 or seat >= len(farms):
        return action
    farm = farms[seat] or {}
    money = _get(farm, "money")
    if money is None:
        return action
    hires = int(_get(farm, "hires_today", 0) or 0)
    cost = 0
    for order in market:
        if order and order[0] == "HIRE":
            cost += _fib(hires)
            hires += 1
    short = cost - money
    if short <= 0:
        return action
    private = _get(obs, "private", {}) or {}
    shed = _get(private, "shed", {}) or {}
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    best = None
    for good in sorted(shed):
        held = int(shed.get(good) or 0)
        price = int(prices.get(good) or 0)
        if held > 0 and price > 0 and (best is None or price > best[1]):
            best = (good, price, held)
    if best is None:
        return action
    good, price, held = best
    units = min(held, int(short // price) + 1)
    if units < 1:
        return action
    action["market"] = [["SELL", good, int(units)]] + market
    return action


_CTX: dict[int, dict[str, Any]] = {}


def agent(observation, configuration=None):
    seat = int(_get(observation, "player", 0) or 0)
    step = int(_get(observation, "step", 0) or 0)
    ctx = _CTX.get(seat)
    if ctx is None or step == 0 or (ctx["step"] >= 0 and step < ctx["step"]):
        ctx = {"route": 0, "step": -1}
        _CTX[seat] = ctx
    if step == DECISION_STEP:
        ctx["route"] = _select_route(observation, seat)
    ctx["step"] = step
    if step < 0 or step >= K_TURNS:
        return {"farmer": ["PASS"], "hands": [], "market": []}
    units, orders = _action_at(ctx["route"], step)
    units, orders = _budget_guard(observation, seat, step, ctx["route"], units, orders)
    action = _to_action(units, orders)
    if L_FINANCE:
        action = _finance(action, observation, seat)
    return action
