"""Moon V187M1: rank-1 complete Ramesh public mode across 30 games; RC5 guards."""
import base64
import copy
import json
import zlib


_ACTIONS = json.loads(zlib.decompress(base64.b85decode('c-q}vO^;hia{Mnk_hI<aAM#DB;qD05P7frFiS?kdSiox-FxH2)Z-)Q7rD=XVzKo2B%zEq|`y_%*k@c#wsxl)ZBY*ktH~;#VzyIy8e}D52zr6YB-RIA5o^Ia!+h6|UU;gv!8(&}k?Js}-_rLzvx7Yu3GyUj~kDtE$kbU--H^2M&Pk;XD)8qF)zyI>)=FR?x-Mg><-ag$t|K;;;_x<_p``O!n+<kof@y*R@{q6l9K787}abJA<l6OCT_~W~eU%%%4<NnRfI=ub)hu!X{Z-1CQ(0=#%%k+7^&c=uL|M>Gy$8TDF`=-N(&W}HNYyNREdGWW--*@_&!$4P;KX-ohyPrRN{Ql2hm+Z^W-yWa*+)p3h{rKfHu@}EP`;zJJA694f`*3()f8hNNKlv|jKJPw$oP8a%j#XHZcVBj&W=nGULwH5t6TE*npQJc4xk}Gpas#JrHpi2ZJ-_HpN-$HhmS;;m%+hp;j*}Tpw>Plu+E}jhPn~A&G{`uGBf|-cH$TeI3jO}ud2_jk!OYG6-_^#Kuh7L%pFg#fHN{bo6K=MMFSt^Z&3*XW^S8|xFI%X><b#cj7A7u(Kegx!!>iI)*Jdn!diI$sOkH?2I(55upXclU>wjy_+j(wIUz<<c<emC2R%fg8P|xqc$vXXQ<a^IAk{Ma*`{&cJ*tnAy>}zLE#U^!qrK39g=EKnr7jQRUHhnl84(Y|d?(yTt-TN<p{{8OLmk%F5{B!WgW?wb^_L7JC>%BYqm2X!F`W@hUT|OVYmS$g^+)bM&73BoCj{m-1YUHb0>omV{!`&VY0r|@I*p(s7JruByOA!$>tj<J}Ger-NY$`B3d6?Lns&P;qj(YTMja%UJ<InRAFm#H7eZKC0JKWyubbH@D`Bqo@`OLMw<~kFTT-It9TISWl%k0DvBaiS~{<hhrv86EFCD?XrVQCE)g}@yR52X?g*}Kg9c6qTDtQ$qsB!H*(4SW%B2~{R8E-Q$$DuEkW+0)&_;HUP&wnl6D9KKmwKF8$Mz&1g{(~HxX&EvQK@b1$;sqr#b;T)`o@K-|)*2JDhIBKZJ$3W5Tl4nuNWXUysTC3AsJBx<SvW+_Foi&7K+6E_S;#EG+ye#I(dxz-EZkyi+26!+oV?o%Hr$EW8c_29&GQUf2`c6saoy2oIb4mu!^Y|s5dxFH}W8W)|9^xZ_pRU=wg=mlZB*BM5P<n0R>9D6)%J|8DzE>d38`Bz%%OJT9<H7A*4GjBAhs!b#wN(d`M5b`qkAgF&kL$*L&m0W>G!`I3CT}sUr<4oxy$t#=9=_{(8Fh391u?CMR~I|7^e!&q07Vm<w0!{P`kY@x4$U=T(ukZd^B9fqHS=dPI!oULyDfk~+nF2o)kHo$emU$M#}9Mt&hej?^_mKdoAu-=y6ElD09KV$ljROxtmx-2pWf|%xBK+zPqmdXoi>+W5?2lSo)sr<$jkK~#bAStK8ok`>_<?IsWUTueL7|wM^GNaHdCVH69RX{atcc`e!9`ojVq&n7EzqP@cc@Dp_pofqm3k48AC)4mdxftNml4I=i}2U@kWfs9zgye3(-<9Z15MdEU!x*G~CzQOI9qJ)q%|3mhdxf(p%2pHlFy4<GE#c&EDwLk)63?yp>C5Zj(53a;ybMFMA$~AG0jv_PQ=(6@a8r+rE)fvHY81_hZ;g3sZkSS{2kbp2;Hc;KT!&?1w(?iJYrmYKJXHGGqWy_Lw6iJvaNw0x{M0WfTgB&SuYNkC$U|S21*MHUk|%;q<6rq6;%h5~0A4o%sPxLPl=Oiy}D454U;U47e0$!N^yGsjl$03z^sGrL#xiplGb*p?<<JBqw*=HJEO%NEDwt1OCcfx^?Tsty_`h+7z;;2=}C9Wa+J(&uo}7ig;zu0|GTst&yGnduE~PTfyye3@}R7Jcol||M>Xvx$0HlSEsR4{@UpaQ@Cz{2;rjm_Uo1TeOig@N3M~};??4&AGff}Fin?{U*VcZmoVL1$S02f!w64}O^(x1kihQ-8>G;qSb^a@L9MFP7%#72E)7Utb|K><1Cx^pJugrPhM(iHBAz^(@BEy(c$PSevB+B22%o<X7~pw<qYE^9Va&_cfaj80S6pzIL<sopdc8hauF2FWQ_Bjh6Q|goMW^r^9Dpna0&cB8TMX4kSA&kFQ{v~?H08e0$@0P6pq-azT&7Re-G?XBXG@j`Shb}(?Kf=BXUNuAwxrIfI}Zr5q9wIU)CYs;QsL`#QHH`G9HJs19j-$i_!n^bsvK8cc&EV4-DV$}2FGn?D#?&Br*-Ng3ON=8TVFg5_GVXw!wHTcUWRoFfkPr8syui?(mE3@5o0>shrd3UEHlO%i0A(49pHJ*|6l2#Jx9ASMm@a++^zYiYM$}=o0BsPpX%9VzykFf5z*Iff#jzk19g|*lGE!8L|uy%fn6ZhIJAS|rT%cXXf(KnC$X>W6o#X`?LzRyIPTu`JM}mD-k}cOVAT(*&LIU|CB?47aF~V>tp=+XS39$kWwD}k1DK+LnrV;XUz?B)TN?%sl#;%TAON2Bl*F@~#|j)^W7_?I!TIe{v~)cwo*1C)cLASVc(Ume(>P{u2*{lVk<?|}viOu6k=WIxk$PDxA?K+gBrCd-F<Ldef@vL?X9Bz{9*a?M(HtH)Dx-T329XNh+$4k($<#dF_J92F@gKj*pkNn0_$YKp%%^<*om;`uoP5esXtmiK$=kI8Nc=}R)p3ySPn<XOOk#E2so7)<%1g&;OPB%j;i7~l#mXq>r|~#j^f-Q+7GxYSk&7#;=D5212%Z|5AE$yKUuBnK!XpiF9V*t{Q(<H1$c?26stciK6@V|Wpf;X-7s9bDDv}2YQ6D}HPm=T)sNbum1;Y|1$mB!>d{Q84#c`c2TU`e%SjfvbYCb$c<k*JGH6*$d#W3~Bs-1rYpNJrq18)^3$iCf`_0u8_4E$yaASEs)2s3!S64B+W03(9m<9^uCQ}Y;8!hBP`#N{8BiBR8ERI^8XCQ^n%*}x!JKU;ox=3Z(t$L0rHSJX8s1;4e~diZTl4afSolD3{?wTGta-kPc~PTv$A6>n6cHi(uq64<wu2iq=e8)W#TB(V6<OB|3RkImWDiLz9YMO~-9avaDZx)R1~<V&l(Kk0|F8oUJ_UT9qt$PT_q7<zJ|JFG#FgN?Xe9K!kbCR}DZJW-4Z;ZT4C#GwI?#2Ao<J5Bbwlf|W=q#PTZ8v2zee@VEz9f^s%0=#C>L2g+6L8B7kK{%~&@vKkjqJ@VciT(x6j+c)a>cNFGkcp+xkTSxnh|P*YqNOq8ho^4efMf+S2@@?Ts}=8xSJ{HM8^BpC85OLbuNbODnN}gdFyQG`y1%(VBTYktePiODFZP^(g1poBvV>rw85r^+hV(|q+SRBbWS0`cKntk4NFHuESy>#)1<Vz?;hu-R<;<i|4lJjqg<ED|ar{jpFUVa57CD$ml*ux9{>J$g>_Ki}`hdRsOObrDT)Ir2yKxKgs;kJrYf#KjnFQ6{YmPel)v4a4DS0q-=Je+}2mK7i%1q&Fq&}kpLV4t<t52)ZxOk`pqyZ4sRFqO7AzRl714VfL9@O;e1J!$fOb(L+LyZ@n-GTS>(Dim;Dn|@l5RVvz$0SPi8}D6X0+`cAK?}Fs9Z<EVOY9>+x7=2mQ&^ZPEZIRZj{;DF{`)k9w^S@%!hnW7y$qxPu}bz)Eanv<+Jc1bch@?c!3+Re5nO6g500Li8e0vFX6hV_9p%-lSMa6Vr@_$*h#Ya2W{BW3P4_wKy#ot`3A@jqzt1E>&))~*1MsUT869)n)Bl0qOLJzI#mWr-IDFmONlbweP_hR2Jh)9kti;h0_8hBqPre$BHHPVQ^Z;cy27Fi2eE~tFinZyOA+z#wB1(gganW@9kq*W&MtlD7`^U$h(rqH86I^uU_G)YuI{OF+NRe;6i|o>(xO6W@UEoFmau?z5tW_SxE7vxJ#irm|_QZffO1nOv7jer=6zz2^BO*C65klyfox|cvvv4!31iJH?UeEvGS=tUfq@&FOS%m89{VmxD*Iq$IWKK;i@*T&Xx}-Og4U5*qk+ZL`yYH^GJ|^(F`<&J7#uB|3TM^@hWmdIHy`dro;TI<%?iN?Ku2u~K;d(U$2b)~Dh+O(;)R?emTT>`PjWk2VA1vdl4X96UYLvQ~{vQa8)F+)s9G5%?Yzc&Q(h4#c`q*^Hu`<*_?w~6A^4kD}f@NA=eVgXu3$~J=A^f9eSJbPpSeW(`8W*U%MSt8mlAAK|-G2l@vXO=fwhEY*YcTZ29$an{C9ESKu27U|uq?-(mKq~hfkf|}|Ht<q{_q0p$EY>Pod=H#{+O``ue%9-)}J*hcx~Aq?3D9AEWMPpNU(CZ`<+jm?v?f<f!qc%N>T}vwlpEIS+m~X<lu_VIJW;cSa{DaSfyyel(luGKua+(z08r$vbuUZy|al%z#<Eeyf#m2yC7-JUxCb|A<@$8X2gRxCWDw_b`qdzl6DR0Y+5zoXB#4`*V<7q(&WB90g4P(V@ZFE)z1#q*0vkzM5yNBRe5?`Va(}*1EGGK8Dn!dprLW9#y%tLxI^}1e#*sSwTz{X#z@5SqV{cDlo8X>%q~$SBt>xBCt9Dkr4Zr9t-{OD20EW|r11m^HuP(7H2IfCVQkt8x+Qbuj@<&M4^KCTJ3+n($hZq{WrHt4s<*|#D)Wv<h1W8{s7VcjVe;wB>&dlf291f=ooT+qqILs$hJLZwX>0+y7?y2e><$#<?mo9$$CKlSd*+tabQ~xEu)rKYIiZleR{h*@&cX`bzRafToQ71HZD_H4ONM?Eot@rofu68?g-H;lIWiusjNDyg8;)|%&~cC|NK-`YyC#1LE5(a4FK?2%MO@3MC3W)nn?k(zmSyIz5&kWkm#3<aV<ku%)yfh+bKwU>ugt9*i$)Q}(;*75C5t@};bS9x^tSW-r3H~vA4P9ch^kgpUz9+H5A4b?0sNmlL~VkSy!?nNE#}(7B_U8|r#U+wS3dk2t!>InO3cej1yH7K1xmcSae;Mb3abt1oum40r67uxJ5@}yOD}anS)sn1mT2YBw**E7!yHG?yJp|Ed#M<{#3ALru12QRW}s&n3z1ozAzZ@)lUn;aG}*&)Ojdb^o;;SeEpyo%v4>`-yHd)C9$IN8e38VgXXsXzr!sY1iH{y?RA_vckOfBDEK?>Vo1Lb-zC{4>Q;|gZwa^3#CB6i|Kx>+_1FYMBoiPe5x#LtArrSi=RFhdGng)C8^^>N-mE{VYF=&n`NH6N%h{$@<j>ynOS@%NY^*~Af^8nXf4TRD@^3v3VsN2?6+4Mvl)&trP3;(y-a_M=;C~}?~uol9E1FvDPSDo&}VTFDLVqNdbN{adXGhBG7NgmKGSzhI%lvE@{PMKk%(V)5Y?r*PfMh}bY#Ml6Zm6W5Mt1>ZyvVD6s8zEniQ=SX$0GfOHR)P}5bgU&cHT~tzs+S@aj@P;&*TsIy*i9Y1UixHAZpKhy7Lr&o3u)$b$B)sb>U$jWrIm8#b|%m_`Zz1@Nv|I8V|kzmPosNFa~{X&H6%sPD!l|_=}V^*95}jk$B4eeE%!){A7{r%sd{BGjmA`VI_xTo)1Xj)!Wu7&s|N9aa^WJ`OQn=UBy>l$G;m$e){c!1g{peLB@bvYE{4-Hlf!Uoad8rhTH+Pp2hgY~sE9qFLPtV=zUXovURKpJDK<fVLeIqQeV{DfAA2I8LNHYQq1x<tYSgVy6<9cT|3_IkIZ_z@!bFtQzu6iZ9cs)?$F(=)3X`*tgQyTYg`gmhN@u)qFOo6!`Bw{(koHbG%Ht)8y0M;Ma>ptb5>nn7z3hR%4Jh(4J@*>Z;z$8p27VV{h2pCCEaofQ$5=6#$v*IlLTJzS7TXK_2-u+jPKy+)NyD+ckBbq@J2RWOqrf?%RVI0NL)}^JR>#r>w;l$bjqcDaZBgL<C6cyYObO05(QnM*@{7C#=WgZc9Tvg(bbi!uaB88fu^&~mF}8k}ZeX3sXd|i9n?;As`fVEPf(bN3#mZc&C1yMg)khI{%s7g5HVQk3GT;bTW&(ROm3IA|!yt4-6e46RX_!{o2s!dM2L2E1)7M%<14P5;P%6Ksz?dnq4|L2!LO>Tau^iQ_S%b%fqM}Uj8nSZF3H9Lkyi={p2Y*Wa6T;Hzu`GBtRQZIYmWlDdJi?<_jxOZ_OG>e$G8;O96AQuy;GpaC$&^rv#{<ieA+vld;wSwcTdNKz^m@Do#^|$}laVgtvXMG9<QuQzkp`4xOpLA=HJS$tnsD7jewm>$l|+{-<8?FZjp`km@~n(e(3iMloy9@m!p_+N*P+34Msc*mQ8%1dy|6T-awQE=!S~3eu95HJUM{}X0=}t8N5v7niXVtkfMay_9m~ulE$yVj66CnlsurOO1lmM+vpXt`Ws5CL?w-ypRYW{@ED<z{_#$2=U85Y776s>LRJa}!^AzncC;=0kYdI6M7!dCAFmU2(Bqxu$(zEj3Vsbuj8q6z#8%pgua@yV(WW{K3O^>NqUj|^MlJ*FSv!7|HPIZ_vNKMj^k@RZa=>dYq*Wq^OUs#*vFhG1qxl^65&ET-uJxHaHkq*piv|IMj!Y@|WR+v(YfpS&IVP6V$sy(SI_{0?%DC-xkugXVJ;2>11)LNt;OPUx6_-|gmUTp!&Je%$a$%yg=Dtl6z=GQaSmzdb-y>%GtOdZ$Cyu98dS0|Guh!y>S=B9T8$*=zxQ|lsokZfJ7StAjcH;bKGsAVv4#zLV?B)8%%10cP&IEz@u6{{fO#Q~?wt)%k`^Xhh1eO!j0mS}-J=n^A7MCZx#!bE-o^FOGQtgsKV!lUU4((MJDWgcAA(-ES^!b<g+oLfv+q0q8XO=1*(7f=A&A4K9{9W4}rt!JChZ#F+xO%#m*>O#Q0AWIdXH6gcguWW`fopyO2CuqJZ`O-?O_?{i=F>UQBwER2!%wl6^GY4o*9u!(B^4&faMhpDF&d%9+f}R7tJ_5N2I%lldi|4;AeYAw?RHkmp?(lhY<^g;!LIJE)eCkuu$3=@)Vnn4nUbPn1qt$!fZw~UgmagV|P5PG6{COiNL>1w%7pmwxa$4u_tiwC27v*S~04kYmt3*MzlYDzcV2I(D7A#5hpQ`1J>z8=UI833%>ndWUUdVV5eMRi56t(!BKP;Im>Ri9(Oi_x5QYWae=!jUgJ0*871w>KYj=z_vTJ3jECDD~|C#$?rtz`pNZ;~I4eTrpnI0(hj=0QH`P`x4Pl`e&-dSS7@0}@#hj!nAa?~X9D!S5rIjwo8X6NsNeRtd1tXe!_cDW;vdm5d8Rg9rkAIa@8JsyI#&aw^%31x0Vc1|+~QNJ4N1k<n_QOR)s!weOK3)w3v9?prROQNNU$4%OE)ukagl?M<OV!C+ifJv-lpO#&u}O!!S!S7C2erBExCUCpusH18tVWwQD%J%Cs|<Pl7%1%llgibjY)x@~}8mI}Yq2N2UpZ=bFPiq+t;daBJvetItuw3gv?Gq<0M1)F%+ZJnIBFcx-{X^Q`2`j-pv>mI;i1?5i@&0<}Pee8?&f=t+erI~?$d5B-L4U@L1Od2Qk<&(R$`|r_-)0UCGwM}Pf+tQ0=ZQwj{p}feXXf4}@X>4P2#j~eUBFaVYA%Qn2ziD7HT%#yh0Q0rLNPW4h0#srq-6e8-<*7pCN(&;3p)__+t(JL9&q#?u$_!j0G6=*Wu_E^w7kRQ01YT+97ylejeaES+8>yd0B$`x<H4XGst`_OKk?NA)_`SIItdO@$5iGY$$k21{ktjoLv6yT<8(Nr03m<szhZd#DRi~@5@o2Mv3_q=#xk=HC=Sc#<WC<!Cd|z_MM!RRcCRPERQpu3PEwl^;@FXf|v2p;9+|_~hgj(8;JF;9tKk~WiMgB<Wi^-??zIiUp?llZ8HO+!p!#cV6X{~cclB+c+065vLDGQ0qE3g)R_>rxgc~Xx%*(?B5dpkh=v#?BbO)*UZ=aD#f(W#L>H{ZCZ0w}TNUPb%<s%$y0Nn@^IW=fYi5ZD!|a#h`K;r!Edozt>XR|vYTbZkj7N-j{c(Ts1xV9%u+ja3)QFKhDijKxwU`N+4$N9I)=)QMwhdq)ec04FW7kXZl+kWuFJDBe!pL%&_NZ9<h?7o6gPj24q`<5xJH#?kX?eYGlh782AB1G~7ZDB1R!ro@RuYUe1L7UdN+ibk(%JBKsGxFHDwOAFXpi-iKc@vwE}u4iInR2PVmY8;J6xPj1~^pzYv`c%rx8|q>p5O1!ACl3?mQvtPcv%o7OHE*=lbErcUfb)_-k0s=Jw0svZ`3Ry~sHiyN>MQO8-MJFjJySZbwcP6<BJ!kBEge{rfJ&k}2ai|d3X8}|iwv9+h<npNQR1efv!Qy72<)X$m|41YSPf+4go>0AQ>GuiZ|Fd64M75ab!72Z4vwXHdhlo}jL_83!~DGM5EQpq&1$);>u*u=&y@Ac8B-fYK8s+Tjk%>Yq)DF)@^~>+&xnegGQ~I}<mj01!Xl)^%7U1VKflrk5<imKPDxb!=8)g$4_uZ830ds|<%w6)&F>?f()_Mes=|!GcbS>QMLUn|D`h3bJVwP5RGxTEl^7H%J``eSECN>ve22ZhoW>n%$4J550jfHRkrEn~G5cg0Qhks1T$29vW=l3`|4g2x*|e=>xI8v07l0NXfloJ8<3_JU)ler(&n8*@Ff?yVr7bNW>Xr=w#E?~<GEi@!LqLe_79?Zs>pShMM>_Z2SNO!GU8mI%McFdH<Yv!tS9uPvpR*{*p?ngpLA`zOx;s;k4mq6Zypv+ZL4N|*#>ZHDWr+3d30=8H+?oFL+Ul<OR>B3FDjbNJRR*NphY>a*pxlf#HDpk_1&l4wR=|TUxR1P8&x3HbygmXFH>FP|G7tl<>cx6-I}srRNy6?sTK4Ya<Byl*fnx?=-vp8AFw?Pg8V<xn*%7`m>kp3|N5ey{lIM4nr94UkmC~Yp)5!DCp~Bm(*tg4S9!;<D!7h&p_+W>2G#yf92u-K^-kNSJg6GUL<-BzjGvoOMT6&QXgwoXVN2<ndvY{7MfA%8M!Wc!FiC<08Q3hE|ONtkQ?a4O#{=*-%8M|!Bdu@~P-f%;ACZ`dH{Ofa-ZL@ardoAL6-93R__M3`g9Wk?ESRsZt!5ZM_x)9QNs7J%)o-3;pIyhpERv=$;-oT!D^)eIQwqUPpl1AVbI;uc~{UR3tj{86oCF;KnRs@w$Qg%BT;bHAKh^`1Pxn$Q4laaQ&)6Tm;BC|w&0!ZM`<}n-quBW#$g87O>9dzT;A}Xg{qLo^^{AT$?7&Jo4Nfi{LRe|I{Cxh)4uT&C+g70l6fAnHF1u5teoQ$j{$m3y15*Y+ga25B?X)r(@)F3|wz8I14ru=C(f6Edw8N1{3x8p%5ME-X579Aj@R8h`xFt*f$&~TWarxV7Hecs<ynDuUVa$cq)%%(wZq%J5h*Gj^ug6Y^MoA72FjfJ`pMh%2g*pe_}hW#*aW`3fT2)V9>T1^a$s`}-OlZVNi$WMg#m#|CH{!HnL0Hw(mb;MWL0b9p({W-6#$IK}aa`++7w0t|t!Y<`4VqdgIYCg=;_7!?ktV9pnA3hGjXBqZ!r?nL0W|uyIDr@!5NVa$tI)+cicdve$gV5_DO`2yOvT$2QPyABN3&6C4Rm!S?0t^9Dm=ajd)IM){ZOpn;7Cb+6St>V#Sz_}ZP%bXUz}tm6{T6t$#D!G8E!;qgX=5r0BPmGB-AL^B^?3=I+%Z;|kh;ekUFxvuNUC5ne$K|<RrFHk^o5ZoF}3o03PM;S4{~!P8nsqA$)zeH=E27d*4WOaE#p}Yw4_=}FQU<8gkH=Qt~gaIDGV`LZWW~`Aqwsj8_hBJxDv#CYsd$m@b*09tUMPH^C|SCL<(tnHX+X0CGY57#8gePjgF|LbTuv9qSAN{JGXWwaFk2#YhOEOmh7!zJb>6B+%(E**SJ-Ed4)vk&JoZw$SULJiNwT<K4n57HQG~+N!{}0C2F;dDn%0LjqD?p=H8ne4py~+(79c&D^_C3?&|t<D#xyY|FLTXC(hDa+W7_1VGSX1t6*GB5L@A%cRL6BWsuQ<t-A(|O$x51m;0l&i94fp+PuSi>?88lh#$lnM1!f7EF9dCNF!&K<5k-V)gWG_%&UWGbA;CQ;^hfbwn{?A2%34UlEzTolf;I4d-;y+Yk}HutEdgno8v(V3SNRB53fLRaPnM5Ay)&Th&`OPPrjB8IM#%G2GeERRrNHirtK@801#)J)iYWn9t7iGRWW`_c%qGs3>DeaP1JNu)hq%ihrd!6jRWZ4c$W&xQ=^+gWY+m9S?sVx2M(;-qw#+IkDneX+(F{D=!Xqtw0X6y6XPi3@$K96R#W|YsyAV24pfX@8nLVZ_KVM{gC3lk66?a@(eFdDo78|v&5QwS6}?5{?m`VI;-_?cz=E00UB~qhS`OS-#`~*guuN8v32t!?4D#oF9tLoGSY=k3Cnz*EW=x*8S}pueZk?XcaKvwjgR`zWIL=YPZ)VwJxoorw6ToT>ruw%%|9QCDOD(A!hiDSdYuu#qx&o-C(lyJL^c;Z%!9Zkyg!SPn`{JF-WHjquBGXVnJ8qIoy0a-59J`=qI}6+ImQtw@f)A-oQi`=Sz!V#~xB?!rK&``8)rC6Em}|{f)>H<9idTa~>g;(|T<3y98&*$hhJ;A-xz`Kiwd8OK{)DYu@;y9hEw7f_f>NrqX`j$rsyeBpc<NdRRCppIQn;@YO=}F?4~L>ushnRJ$d;L?TF-DPfzP93#G`Ogpu}%^pgj#D)OD<Y1|*HKifO>dv^r>dJZqQ4(d6LoEf<d`(^v&YkA?51@vK%Uo{M&p8whQ@*Q++^J_}v>g{D+63F?#dt42>%jbTX*mBYREn#z)cum*2ZxCa0Rl%z#-3$?w-sP~Lq!_Q^I7h0qQkJck7Hqo9mhn9SR%~M4!)va@5D2z#yY8Q&A{a%s5Z0XICY6YxpOhJ8%rvrt93LSUjn%e+nwZ6$!SCpJ4u)E5-E+u7!7Hc%+U^KKGEP6z{Yhn&X99lF~poq;Ybnf5{J5p_kTTdIp(L}Bw5v{(0)k2U6gw@0!M1J&&9cGv5CFlSTlyRUU%%afcbg*|%%fxg0MwbrJ<s-*dYUi=|nWRW|5>;-!($ccX=;}@rn#kUXUN{iQL<1$oB&7yx442>(0px&?l(Wi^s0xLyP1niPAokEg^1e1-Uz*Yk_8D7_ge#?_8B@m-Z5cUBsGt#m6dt)qfRI)xmssdA+QMkZ{p@j^b0QTL%ylb#kFM8u`W7r{QVJ9SuL>g(=zM{#T|lc_Sickt>+Z*(Rl#YI{oM_Tmw<|qrqm;)iJ-e;L9s1Pc%a*hAtb=N7|Qc&?IsGL@%&b~UGJ*U5s+TGS<#UrzU3o3jNye^ocWf*lxA3zQyVNYkFAuW<xOmyqNjS>W_W(7oK}Kl0D59Eaoa6D*^@_bTCVc@fFV@vE~m3>!QF2KD2ZBz1PMt+DhW8UtrnfEyCBH<za32S;=N^sHBd!MPn=GD#=}&?gBMad`Zy&yK;-h6$&N)*C~<5@I}UFIayYo%8m0HGE~%!_YMmN)NfeQdov2-$)Brl&U&E}YA6g_sp$Z^ZDvfI9BEyp{)Cd-Yg2En-!#Ms608M|QiS%Ki=?5!v7NUeZ+5ax)+_z6X0Y|gy#-zGS$AGj2Q7VEQR=l`-g2k_Up~HGs^a@%`9SY%BPvbEiCm_<?e4LwH{pTQf^R|@r*0>X=6;Uj(C!flMTY0xqwGgRNnC{%QdTMubDK4;`zcBLw(I8kP>PNou5d@gl3X#*O(-rHs?o80orrN{(_NmZBSk*~Tash()eLlo-4vt>*t!i^zX<i$fwt(@IfOs+}@SYF-vMEYTgTe!L-w9Cwg?gp1$Q=?&;IJDlI`&Tg&t{*{-iRExx7g=&WPla0<MuVc4i>YLi)C*}u|q+iB@mAFi^3Ig)00j~pt_bRxqC_+9+)#i1nJHMN@&GTotra#di<&U^b0&5>selFYbvUhW}I3-h-hqp%JMR$J}PJCA~BX5@tRWrZ&fMiz{4)8jm=xX_gG&tj-;Imv=?Ts>~)@oiiNoP`O+B%D|Myk0h`XQ4Oct|rcidhCxUxO(eFh>Cko?dSBG0dGjdV@tq);_LVLoD$(Fh@#?8=PJkfTuNfYT*`1AI0C%?lyln;#V0&Kdc*9hmV$-bLSJep+8I9-j5$RU9+)Pe;Ud<aQH7P}q-jB1k8y>v`f$q|(#EgV_*fo2<OmJcJFN?0Gq%6&7g!zr_nR&(Ej2Ec9UDwo+2G;;9J)cew-zU!+6qF1K@o?hsth~krV)e>M<N9fBbhNnLWkI{I-#?M%lLcyl)S&VN<`6+Frr3;Mg<q{ay<wu|X7ZW|+7y')).decode('utf-8'))
_FR_ITEMS = ('MELON', 'MILK', 'STRAWBERRY', 'WOOL')
_FR_STATE = {
    0: {"last_step": -1, "due_step": -1, "due": {}},
    1: {"last_step": -1, "due_step": -1, "due": {}},
}
_WEED_STATE = {0: {}, 1: {}}
_WEED_REPLAY_STEPS = 8
_SHOP_PRODUCTS = {
    "BAKERY": ("EGG", "WHEAT"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}


def _get(value, key, default=None):
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _copy_action(action):
    action = copy.deepcopy(action or {})
    return {
        "farmer": list(action.get("farmer") or ["PASS"]),
        "hands": [list(order or ["PASS"]) for order in (action.get("hands") or [])],
        "market": [list(order) for order in (action.get("market") or [])],
    }


def _seat(obs):
    return 1 if int(_get(obs, "player", 0) or 0) == 1 else 0


def _farm(obs, seat):
    farms = list(_get(obs, "farms", []) or [])
    return farms[seat] if seat < len(farms) else {}


def _align_hands(action, obs):
    action = _copy_action(action)
    expected = len(_get(_farm(obs, _seat(obs)), "hands", []) or [])
    hands = list(action.get("hands") or [])
    if len(hands) < expected:
        hands.extend([["PASS"] for _ in range(expected - len(hands))])
    action["hands"] = [list(order or ["PASS"]) for order in hands[:expected]]
    return action


def _tile_at(farm, position):
    try:
        x, y = int(position[0]), int(position[1])
        return (_get(farm, "tiles", []) or [])[y][x]
    except (IndexError, TypeError, ValueError):
        return "LOCKED"


def _trace_actor_action(step, actor):
    trace = _ACTIONS[min(max(int(step), 0), len(_ACTIONS) - 1)] or {}
    if actor == "farmer":
        return list(trace.get("farmer") or ["PASS"])
    hands = trace.get("hands", []) or []
    return list(hands[actor] if actor < len(hands) else ["PASS"])


def _weed_repair_action(obs, action, step):
    action = _align_hands(action, obs)
    seat = _seat(obs)
    game = _WEED_STATE[seat]
    if step == 0 or step < int(game.get("last_step", -1)):
        game = {"last_step": step, "active": {}}
        _WEED_STATE[seat] = game
    game["last_step"] = step
    farm = _farm(obs, seat)
    positions = [_get(farm, "farmer"), *list(_get(farm, "hands", []) or [])]
    unit_actions = [action.get("farmer", ["PASS"]), *list(action.get("hands") or [])]
    active = game.setdefault("active", {})

    for actor, transaction in list(active.items()):
        index = 0 if actor == "farmer" else int(actor) + 1
        if index >= len(unit_actions):
            active.pop(actor, None)
            continue
        age = step - int(transaction["start"])
        if age == 1:
            unit_actions[index] = list(transaction["intended"])
        elif 2 <= age <= 1 + _WEED_REPLAY_STEPS:
            unit_actions[index] = _trace_actor_action(step - 1, actor)
        else:
            active.pop(actor, None)

    for index, (position, intended) in enumerate(zip(positions, unit_actions)):
        actor = "farmer" if index == 0 else index - 1
        if actor in active or not isinstance(intended, list) or not intended:
            continue
        if intended[0] not in ("BUILD_PASTURE", "PLANT"):
            continue
        tile = _tile_at(farm, position)
        if not isinstance(tile, dict) or tile.get("kind") != "WEED":
            continue
        active[actor] = {"start": step, "intended": list(intended)}
        unit_actions[index] = ["DIG"]

    action["farmer"] = unit_actions[0] if unit_actions else ["PASS"]
    action["hands"] = unit_actions[1:]
    return _align_hands(action, obs)


def _fr_state(obs, step):
    seat = _seat(obs)
    state = _FR_STATE[seat]
    if step == 0 or step < int(state.get("last_step", -1)):
        state = {"last_step": step, "due_step": -1, "due": {}}
        _FR_STATE[seat] = state
    state["last_step"] = step
    if 0 <= int(state.get("due_step", -1)) < step:
        state["due_step"], state["due"] = -1, {}
    return state


def _town_demand_now(obs, item, step):
    demand = 1 if item != "FERTILIZER" and step % 24 == 0 else 0
    if step % 4 != 0:
        return demand
    town = _get(obs, "town", {}) or {}
    for shop in list(_get(town, "unlocked_shops", []) or []):
        products = _SHOP_PRODUCTS.get(shop, ())
        if item in products:
            demand += 2 if len(products) == 1 else 1
    return demand


def _future_quantity(step, item):
    future = step + 1
    if not 0 <= future < len(_ACTIONS):
        return 0
    return sum(
        max(0, int(order[2]))
        for order in (_ACTIONS[future].get("market") or [])
        if len(order) >= 3 and order[0] == "SELL" and order[1] == item
    )


def _pickup_reserve(action, item):
    reserve = 0
    for order in [action.get("farmer", ["PASS"]), *list(action.get("hands") or [])]:
        if isinstance(order, (list, tuple)) and len(order) >= 2 and order[0] == "PICKUP" and order[1] == item:
            try:
                reserve += max(0, int(order[2])) if len(order) >= 3 else 1
            except (TypeError, ValueError):
                reserve += 1
    return reserve


def _existing_sell(action, item):
    return sum(
        max(0, int(order[2]))
        for order in (action.get("market") or [])
        if len(order) >= 3 and order[0] == "SELL" and order[1] == item
    )


def _repay(action, state, step):
    if int(state.get("due_step", -1)) != step:
        return action
    due = {str(item): max(0, int(quantity)) for item, quantity in dict(state.get("due", {})).items()}
    action = _copy_action(action)
    market = []
    for raw in action.get("market") or []:
        order = list(raw)
        if len(order) >= 3 and order[0] == "SELL" and order[1] in due and due[order[1]] > 0:
            requested = max(0, int(order[2]))
            reduction = min(requested, due[order[1]])
            requested -= reduction
            due[order[1]] -= reduction
            if requested <= 0:
                continue
            order[2] = requested
        market.append(order)
    action["market"] = market[:10]
    state["due_step"], state["due"] = -1, {}
    return action


def _front_run(action, obs, state, step):
    if not _FR_ITEMS:
        return action
    private = _get(obs, "private", {}) or {}
    shed = _get(private, "shed", {}) or {}
    moved = {}
    action = _copy_action(action)
    for item in _FR_ITEMS:
        target = _future_quantity(step, item)
        if target <= 0 or _town_demand_now(obs, item, step) > 0:
            continue
        stock = max(0, int(_get(shed, item, 0) or 0))
        reserve = _pickup_reserve(action, item) + _existing_sell(action, item)
        quantity = min(target, max(0, stock - reserve))
        if quantity <= 0:
            continue
        market = [list(order) for order in (action.get("market") or [])]
        existing = next((order for order in market if len(order) >= 3 and order[0] == "SELL" and order[1] == item), None)
        if existing is not None:
            existing[2] = max(0, int(existing[2])) + quantity
        elif len(market) < 10:
            market.append(["SELL", item, quantity])
        else:
            continue
        action["market"] = market[:10]
        moved[item] = moved.get(item, 0) + quantity
    if moved:
        state["due_step"] = step + 1
        state["due"] = moved
    return action


def agent(obs):
    try:
        step = min(max(0, int(_get(obs, "step", 0) or 0)), len(_ACTIONS) - 1)
        action = _weed_repair_action(obs, _copy_action(_ACTIONS[step]), step)
        state = _fr_state(obs, step)
        action = _repay(action, state, step)
        action = _front_run(action, obs, state, step)
        return _align_hands(action, obs)
    except Exception:
        farm = _farm(obs, _seat(obs))
        return {
            "farmer": ["PASS"],
            "hands": [["PASS"] for _ in (_get(farm, "hands", []) or [])],
            "market": [],
        }
