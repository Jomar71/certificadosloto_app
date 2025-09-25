--
-- PostgreSQL database dump
--

\restrict GbO0Y28bo1kapDqf7mNLtOfTDnt1hN8dn1AKxDLJ35OBfBsHCiayXbB7fztWNPn

-- Dumped from database version 16.10
-- Dumped by pg_dump version 16.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: certificadosloto; Type: TABLE DATA; Schema: public; Owner: usuario_loto
--

COPY public.certificadosloto (id_documento, tipo_documento, nombre_persona, apellido_persona, numero_identificacion, fecha_creacion, fecha_vencimiento, ruta_pdf, email_persona) FROM stdin;
174	Cédula	michael	villasmil soto	1414827	2025-04-18	2026-04-18	certificado_1414827_174.pdf	\N
176	Cédula	adarlin valladares	krismari caceres	3176897	2025-04-04	2026-04-04	certificado_3176897_176.pdf	\N
177	Cédula	marisabel	duran teran 	4548569	2025-04-18	2026-04-18	certificado_4548569_177.pdf	\N
178	Cédula	ericson	oquendo	4624092	2025-02-18	2026-02-18	certificado_4624092_178.pdf	\N
180	Cédula	Douglas Jose	Medina Fuentes	4876803	2025-04-14	2026-04-14	certificado_4876803_180.pdf	\N
181	Cédula	noramis	arrieta	5165202	2025-04-04	2026-04-04	certificado_5165202_181.pdf	\N
182	Cédula	Lilibeth Isabel	Medina Alvarado	5220596	2025-04-14	2026-04-14	certificado_5220596_182.pdf	\N
184	Cédula	ANGELA MARIAN	ZAMBRANO 	5302995	2025-01-24	2026-01-24	certificado_5302995_184.pdf	\N
185	Cédula	LESLY NELSY	REYES CARVAJAL	5327772	2025-05-08	2026-05-08	certificado_5327772_185.pdf	\N
186	Cédula	gerardo 	briceño	5462512	2025-05-15	2026-05-15	certificado_5462512_186.pdf	\N
188	Cédula	ana carina 	perozo henriquez 	5870179	2025-06-19	2026-06-19	certificado_5870179_188.pdf	\N
189	Cédula	JENNIRE ALEJANDRA 	BLANCO GONZALEZ	6092529	2025-04-23	2026-04-23	certificado_6092529_189.pdf	\N
190	Cédula	eddymar soliannys 	rangel 	6239519	2025-04-18	2026-04-18	certificado_6239519_190.pdf	\N
192	Cédula	geyson jose 	berrios	6483328	2025-02-18	2026-02-18	certificado_6483328_192.pdf	\N
193	Cédula	anssony miguel	melendez calcurian	6676877	2025-05-21	2026-05-21	certificado_6676877_193.pdf	\N
195	Cédula	anyelis	zerpa 	6723044	2025-03-12	2026-03-12	certificado_6723044_195.pdf	\N
196	Cédula	edrick elie	itriago itriago	6786612	2025-04-18	2026-04-18	certificado_6786612_196.pdf	\N
197	Cédula	KEILY JOSEANNY	DURAN GONZALEZ 	6849827	2025-05-07	2026-05-07	certificado_6849827_197.pdf	\N
199	Cédula	jimmy	peña peñaloza	6924932	2025-04-04	2026-04-04	certificado_6924932_199.pdf	\N
200	Cédula	Slecnia Alejranda	Hernandez Saavedra	7044259	2025-05-07	2026-05-07	certificado_7044259_200.pdf	\N
201	Cédula	daritza oscarina 	rodriguez arroyo 	7357054	2025-04-18	2026-04-18	certificado_7357054_201.pdf	\N
203	Cédula	DIEGO JUAN	VELEZ	11793359	2025-04-23	2026-04-23	certificado_11793359_203.pdf	\N
204	Cédula	marisol	josefina	12379845	2025-05-19	2026-05-19	certificado_12379845_204.pdf	\N
205	Cédula	WILIAM ENRIQUE	BELEÑO ROMERO	14164183	2025-05-08	2026-05-08	certificado_14164183_205.pdf	\N
207	Cédula	jhon jairo 	garcia rios 	15612540	2025-06-19	2026-06-19	certificado_15612540_207.pdf	\N
208	Cédula	JESUS 	EDUARDO MENDEZ	17640370	2025-07-07	2026-07-07	certificado_17640370_208.pdf	\N
209	Cédula	MOISES	PAREDES	19843635	2025-05-07	2026-05-07	certificado_19843635_209.pdf	\N
211	Cédula	blanca nubia 	perez	21469209	2025-02-18	2026-02-18	certificado_21469209_211.pdf	\N
212	Cédula	natalia andrea 	orozco 	21527185	2025-05-19	2026-05-19	certificado_21527185_212.pdf	\N
214	Cédula	PIEDAD MARIA	TORRES VALENCIA	22118268	2025-07-07	2026-07-07	certificado_22118268_214.pdf	\N
215	Cédula	MARIA DE LOS ANGELES 	MARTINEZ	22710948	2025-06-24	2026-06-24	certificado_22710948_215.pdf	\N
217	Cédula	ANGELICA	NAVA	24267145	2025-02-21	2026-02-21	certificado_24267145_217.pdf	\N
218	Cédula	yoela lucia 	soto vega 	25878721	2025-05-15	2026-05-15	certificado_25878721_218.pdf	\N
219	Cédula	MICHEL ESTEFANY	PAZ RAMIREZ	26240131	2025-04-23	2026-04-23	certificado_26240131_219.pdf	\N
221	Cédula	nelymar 	chirinos arrieta	26813406	2025-05-20	2026-05-20	certificado_26813406_221.pdf	\N
222	Cédula	angel	pirela	26923157	2025-04-14	2026-04-14	certificado_26923157_222.pdf	\N
223	Cédula	carlos 	sanchez	27550856	2025-04-14	2026-04-14	certificado_27550856_223.pdf	\N
225	Cédula	YENIFER CAROLINA 	PORTILLO MALDONADO	28110155	2025-05-08	2026-05-08	certificado_28110155_225.pdf	\N
226	Cédula	LUIS ENRIQUE	BELEÑO ASTUDILLO	29537592	2025-05-08	2026-05-08	certificado_29537592_226.pdf	\N
228	Cédula	yusbely 	montilla 	29944224	2025-04-14	2026-04-14	certificado_29944224_228.pdf	\N
229	Cédula	JOSE MANUEL	VASQUEZ HERNANDEZ	30457658	2025-07-07	2026-07-07	certificado_30457658_229.pdf	\N
230	Cédula	diego rafael 	escalante godoy	30536246	2025-06-19	2026-06-19	certificado_30536246_230.pdf	\N
232	Cédula	DIANNY MARCELA	CASTILLO	30779235	2025-06-24	2026-06-24	certificado_30779235_232.pdf	\N
233	Cédula	pedro javier 	marquez gaura	30881307	2025-05-20	2026-05-20	certificado_30881307_233.pdf	\N
235	Cédula	lisdiani	sanchez 	31704467	2025-06-19	2026-06-19	certificado_31704467_235.pdf	\N
236	Cédula	JOANDRY SAUL	PITRE GARCIA	31932140	2025-02-21	2026-02-21	certificado_31932140_236.pdf	\N
238	Cédula	jaqueline	lopez urrego	32290795	2025-05-21	2026-05-21	certificado_32290795_238.pdf	\N
239	Cédula	damaris 	martinez nova	32778111	2025-06-19	2026-06-19	certificado_32778111_239.pdf	\N
240	Cédula	yuleinis yelimar	alvarado diaz	32914267	2025-06-13	2026-06-13	certificado_32914267_240.pdf	\N
242	Cédula	GLORIA 	BERMUDEZ	40730955	2025-04-04	2026-04-04	certificado_40730955_242.pdf	\N
243	Cédula	ANA	LOPEZ	43156415	2025-02-15	2026-02-15	certificado_43156415_243.pdf	\N
245	Cédula	gabriela	manco manco	43532714	2025-03-12	2026-03-12	certificado_43532714_245.pdf	\N
246	Cédula	claudia maria	muñoz rios 	43635315	2025-06-19	2026-06-19	certificado_43635315_246.pdf	\N
247	Cédula	MAYDEE PATRICIA 	LEAL RESTREPO 	43652855	2025-01-24	2026-01-24	certificado_43652855_247.pdf	\N
249	Cédula	claudia maria 	hinestroza cortes	43717745	2025-05-06	2026-05-06	certificado_43717745_249.pdf	\N
250	Cédula	Elizabeth 	Serna Salazar	43787996	2025-05-07	2026-05-07	certificado_43787996_250.pdf	\N
252	Cédula	monica alejandra 	diaz correa 	43972880	2025-05-06	2026-05-06	certificado_43972880_252.pdf	\N
253	Cédula	Teresa de Jesus	Pamplona	43973680	2025-05-07	2026-05-07	certificado_43973680_253.pdf	\N
254	Cédula	diana marcela 	mayo rios 	43997003	2025-06-19	2026-06-19	certificado_43997003_254.pdf	\N
256	Cédula	Maritza Cristina	Sanchez Monsalve	63527818	2025-05-07	2026-05-07	certificado_63527818_256.pdf	\N
321	Cédula	PAOLA ALEXANDRA 	CERON PANTOJA	1085287245	2025-05-08	2026-05-08	certificado_1085287245_321.pdf	\N
172	Cédula	yusmary 	padron sevilla	1283272	2025-06-13	2026-06-13	certificado_1283272_172.pdf	\N
298	Cédula	camila 	osorio 	1036663328	2025-05-06	2026-05-06	certificado_1036663328_298.pdf	\N
323	Cédula	CAMILO ANDRES 	TARAZONA ORTIZ	1094575017	2025-04-04	2026-04-04	certificado_1094575017_323.pdf	\N
259	Cédula	jaime alberto	arias cardona	71241968	2025-04-04	2026-04-04	certificado_71241968_259.pdf	\N
260	Cédula	jorge alirio 	jaramillo jaramillo	71376290	2025-06-13	2026-06-13	certificado_71376290_260.pdf	\N
261	Cédula	CARLOS 	ARROYAVE	71379037	2025-02-15	2026-02-15	certificado_71379037_261.pdf	\N
263	Cédula	walter alexander 	perez neyra 	71772270	2025-04-24	2026-04-24	certificado_71772270_263.pdf	\N
264	Cédula	WILMER ALCIDES	PALACIOS	71946659	2025-05-08	2026-05-08	certificado_71946659_264.pdf	\N
266	Cédula	Rodrigo  Rafael	Ruiz Rosario	78575992	2025-05-07	2026-05-07	certificado_78575992_266.pdf	\N
267	Cédula	jaime albeiro	marin marin	98472210	2025-05-22	2026-05-22	certificado_98472210_267.pdf	\N
269	Cédula	xiomara alexandra 	marquez sanchez	1000638335	2025-06-13	2026-06-13	certificado_1000638335_269.pdf	\N
270	Cédula	kiara patricia 	perez sierra	1000887170	2025-03-12	2026-03-12	certificado_1000887170_270.pdf	\N
272	Cédula	laura valentina	rodriguez 	1001235093	2025-05-06	2026-05-06	certificado_1001235093_272.pdf	\N
273	Cédula	anyi caterine 	betancur sepulveda	1001387307	2025-05-21	2026-05-21	certificado_1001387307_273.pdf	\N
274	Cédula	SARAY MICHEL 	GUTIERREZ SALDARRIAGA	1001445382	2025-05-07	2026-05-07	certificado_1001445382_274.pdf	\N
276	Cédula	DIANA 	VANEGAS 	1002105759	2025-05-28	2026-05-28	certificado_1002105759_276.pdf	\N
277	Cédula	osneider	tarazona ortiz	1005075650	2025-05-19	2026-05-19	certificado_1005075650_277.pdf	\N
278	Cédula	sebastian 	cardenas cardenas 	1005321379	2025-05-20	2026-05-20	certificado_1005321379_278.pdf	\N
280	Cédula	angie lorena	florez bustos 	1006433639	2025-04-18	2026-04-18	certificado_1006433639_280.pdf	\N
281	Cédula	JULIAN 	JARAMILLO VALENCIA	1007421473	2025-04-23	2026-04-23	certificado_1007421473_281.pdf	\N
283	Cédula	YEINER	TARAZONA ORTIZ	1007670557	2025-04-04	2026-04-04	certificado_1007670557_283.pdf	\N
284	Cédula	gerardo andres 	buelvas zuñiga	1010159538	2025-05-15	2026-05-15	certificado_1010159538_284.pdf	\N
285	Cédula	MARIA FERNANDA	PALACIO MARTINEZ	1015068082	2025-05-07	2026-05-07	certificado_1015068082_285.pdf	\N
287	Cédula	LUISA	LOPEZ	1017124590	2025-02-15	2026-02-15	certificado_1017124590_287.pdf	\N
288	Cédula	JUAN DAVID	BENAVIDES	1017128512	2025-05-07	2026-05-07	certificado_1017128512_288.pdf	\N
289	Cédula	sandra 	restrepo villa 	1017144838	2025-05-20	2026-05-20	certificado_1017144838_289.pdf	\N
291	Cédula	YURI YURLEY 	MARTINEZ VALLE	1017185424	2025-05-08	2026-05-08	certificado_1017185424_291.pdf	\N
292	Cédula	dayana	marulanda echeverri	1018234494	2025-03-18	2026-03-18	certificado_1018234494_292.pdf	\N
294	Cédula	luis	davila garces	1020501264	2025-02-18	2026-02-18	certificado_1020501264_294.pdf	\N
295	Cédula	MARIANA	SANCHEZ	1027660886	2025-02-15	2026-02-15	certificado_1027660886_295.pdf	\N
297	Cédula	paula andrea 	ossa ortega	1036634812	2025-02-18	2026-02-18	certificado_1036634812_297.pdf	\N
299	Cédula	CINDY YULIET	RAMIREZ SUAREZ	1037660178	2025-07-07	2026-07-07	certificado_1037660178_299.pdf	\N
301	Cédula	cristian david 	yepez arbelaez	1038418181	2025-02-18	2026-02-18	certificado_1038418181_301.pdf	\N
302	Cédula	HECTOR MANUEL	BAUTISTA 	1039082108	2025-07-07	2026-07-07	certificado_1039082108_302.pdf	\N
303	Cédula	ANDRES DAVID 	BARON CORREA	1039101124	2025-05-07	2026-05-07	certificado_1039101124_303.pdf	\N
305	Cédula	NAYERLY	CARRASQUILLA	1039682157	2025-02-21	2026-02-21	certificado_1039682157_305.pdf	\N
306	Cédula	JERONIMO	QUINTERO	1040180025	2025-02-15	2026-02-15	certificado_1040180025_306.pdf	\N
308	Cédula	IRIS 	CARDONA ARROYO	1041265435	2025-07-07	2026-07-07	certificado_1041265435_308.pdf	\N
309	Cédula	valentina michel 	herrera acelas 	1041692717	2025-04-24	2026-04-24	certificado_1041692717_309.pdf	\N
310	Cédula	wilman simon	madero de arco	1044907680	2025-06-13	2026-06-13	certificado_1044907680_310.pdf	\N
312	Cédula	LILIA CRISTINA 	GARCIA LAMBRAÑO	1052987718	2025-05-08	2026-05-08	certificado_1052987718_312.pdf	\N
313	Cédula	kevin santiago 	bolaños muñoz	1061715144	2025-05-06	2026-05-06	certificado_1061715144_313.pdf	\N
315	Cédula	luisa del carmen 	vargas montes	1063146527	2025-05-07	2026-05-07	certificado_1063146527_315.pdf	\N
316	Cédula	manuel 	ochoa	1065615568	2025-06-19	2026-06-19	certificado_1065615568_316.pdf	\N
317	Cédula	karen 	durango 	1066515726	2025-05-20	2026-05-20	certificado_1066515726_317.pdf	\N
319	Cédula	MARIA CAMILA	BRAVO RAMOS	1075090973	2025-07-07	2026-07-07	certificado_1075090973_319.pdf	\N
320	Cédula	yuliana	martinez padilla	1081786489	2025-05-20	2026-05-20	certificado_1081786489_320.pdf	\N
322	Cédula	victor johany	ramirez quiceno	1087489024	2025-05-19	2026-05-19	certificado_1087489024_322.pdf	\N
324	Cédula	ALYANIR 	NAVARRO ORTIZ 	1094580788	2025-05-28	2026-05-28	certificado_1094580788_324.pdf	\N
326	Cédula	jean carlos 	atencia arrieta 	1099992992	2025-04-24	2026-04-24	certificado_1099992992_326.pdf	\N
327	Cédula	antony rafael 	peralta bello	1102876077	2025-06-13	2026-06-13	certificado_1102876077_327.pdf	\N
330	Cédula	kathy luz	buelvas zuñiga	1104873839	2025-05-15	2026-05-15	certificado_1104873839_330.pdf	\N
331	Cédula	ANDREA PAOLA	CAPERA LIMA	1109842936	2025-05-07	2026-05-07	certificado_1109842936_331.pdf	\N
333	Cédula	deyvy alexander 	torres arboleda	1112789742	2025-03-12	2026-03-12	certificado_1112789742_333.pdf	\N
334	Cédula	carlos andres 	orozco quiroz	1113652182	2025-05-19	2026-05-19	certificado_1113652182_334.pdf	\N
336	Cédula	jesus alberto 	gonzales gomez	1114120816	2025-04-18	2026-04-18	certificado_1114120816_336.pdf	\N
338	Cédula	JHOAN CAMILO	VELEZ PALACIO	1125716655	2025-05-08	2026-05-08	certificado_1125716655_338.pdf	\N
340	Cédula	sandra 	guizado zapata 	1128384091	2025-03-12	2026-03-12	certificado_1128384091_340.pdf	\N
173	Cédula	gabriela mirelis	gonzalez ponce 	1369794	2025-05-06	2026-05-06	certificado_1369794_173.pdf	\N
341	Cédula	MAURICIO 	ALDANA GUIRAL	1128402009	2025-06-24	2026-06-24	certificado_1128402009_341.pdf	\N
170	Cédula	Yesica Kirmar	Camacho Camacho	884067	2025-05-07	2026-05-07	certificado_884067_170.pdf	\N
343	Cédula	maria fernanda 	ospina molina	1130268494	2025-03-18	2026-03-18	certificado_1130268494_343.pdf	\N
345	Cédula	luis mateus	caballero lopez	1148435819	2025-05-19	2026-05-19	certificado_1148435819_345.pdf	\N
332	Cédula	alexander	moreno ortiz	1111194219	2025-04-04	2026-04-04	certificado_1111194219_332.pdf	\N
349	Cédula	YENIFER 	CABARCAS MANJARRES	1193509818	2025-05-08	2026-05-08	certificado_1193509818_349.pdf	\N
344	Cédula	gregoria lucia	marios bastidas	1143254390	2025-05-19	2026-05-19	certificado_1143254390_344.pdf	\N
328	Cédula	katlyn regina 	andrade regino	1102877251	2025-03-18	2026-03-18	certificado_1102877251_328.pdf	\N
350	Cédula	juliana	sepulveda osorio	1214746795	2025-03-12	2026-03-12	certificado_1214746795_350.pdf	\N
335	Cédula	katerin vanessa 	moreno	1113657344	2025-05-19	2026-05-19	certificado_1113657344_335.pdf	\N
329	Cédula	LUISA	RAMIREZ	1104422447	2025-05-28	2026-05-28	certificado_1104422447_329.pdf	\N
339	Cédula	vielis paola	cantillo escorcia	1128105735	2025-04-04	2026-04-04	certificado_1128105735_339.pdf	\N
348	Cédula	yesica carolina 	vital babilonia 	1193147074	2025-05-06	2026-05-06	certificado_1193147074_348.pdf	\N
346	Cédula	juan carlos 	morales tabarquino 	1152185770	2025-04-18	2026-04-18	certificado_1152185770_346.pdf	\N
171	Cédula	ANYAMAR ANTONIETA	PULIDO APONTE	1113852	2025-05-07	2026-05-07	certificado_1113852_171.pdf	\N
175	Cédula	adrianis elineth	castillo manzanares	2102400	2025-06-13	2026-06-13	certificado_2102400_175.pdf	\N
179	Cédula	NEIDALY DEL CARMEN 	BRICEÑO 	4704991	2025-04-23	2026-04-23	certificado_4704991_179.pdf	\N
183	Cédula	darwin jose 	navas castro	5222215	2025-04-24	2026-04-24	certificado_5222215_183.pdf	\N
187	Cédula	angi cardina 	gomez zapata 	5480093	2025-04-24	2026-04-24	certificado_5480093_187.pdf	\N
191	Cédula	rosangel 	padilla	6353050	2025-06-19	2026-06-19	certificado_6353050_191.pdf	\N
194	Cédula	YONATHAN EDUARDO	GALLARDO GONZALEZ	6695118	2025-05-07	2026-05-07	certificado_6695118_194.pdf	\N
198	Cédula	YOHANA DAYANA	ORELLANA SIERRA	6897691	2025-05-07	2026-05-07	certificado_6897691_198.pdf	\N
202	Cédula	Alexander 	Martinez	11038314	2025-05-07	2026-05-07	certificado_11038314_202.pdf	\N
206	Cédula	adrian de jesus 	ochoa 	15442016	2025-06-13	2026-06-13	certificado_15442016_206.pdf	\N
210	Cédula	alba luz	castro serrato 	20830922	2025-06-19	2026-06-19	certificado_20830922_210.pdf	\N
213	Cédula	piedad Doriela	Echavarria Barbaran	21969833	2025-05-07	2026-05-07	certificado_21969833_213.pdf	\N
216	Cédula	nancy stella	monsalve lizarazo	22732684	2025-06-13	2026-06-13	certificado_22732684_216.pdf	\N
220	Cédula	maria gabriela 	lopez 	26339808	2025-06-19	2026-06-19	certificado_26339808_220.pdf	\N
224	Cédula	xiomara marina	zerpa hidalgo 	28095652	2025-06-13	2026-06-13	certificado_28095652_224.pdf	\N
227	Cédula	francis kathiusca 	mireles amaro 	29724331	2025-05-20	2026-05-20	certificado_29724331_227.pdf	\N
231	Cédula	hector 	escalona 	30734423	2025-05-06	2026-05-06	certificado_30734423_231.pdf	\N
234	Cédula	YEXIRE ANAHI	DURAN FLORES	31053148	2025-07-07	2026-07-07	certificado_31053148_234.pdf	\N
237	Cédula	NELLYS DEL CARMEN	CONTRERAS	32272168	2025-07-07	2026-07-07	certificado_32272168_237.pdf	\N
241	Cédula	kevin 	hernandez	33770373	2025-06-19	2026-06-19	certificado_33770373_241.pdf	\N
244	Cédula	beatriz adriana	giraldo castaño	43190325	2025-05-19	2026-05-19	certificado_43190325_244.pdf	\N
248	Cédula	LUZ MARY	CANO RESTREPO 	43656738	2025-01-24	2026-01-24	certificado_43656738_248.pdf	\N
251	Cédula	RUTH YANETH	GIRARDO DUARTE 	43818625	2025-06-24	2026-06-24	certificado_43818625_251.pdf	\N
255	Cédula	DIANA 	CARMONA	52529678	2025-02-15	2026-02-15	certificado_52529678_255.pdf	\N
257	Cédula	diana ximena	rojas sarria	66784202	2025-04-04	2026-04-04	certificado_66784202_257.pdf	\N
258	Cédula	pedro nel 	carmona 	70752821	2025-05-06	2026-05-06	certificado_70752821_258.pdf	\N
262	Cédula	LUIS	TORO	71722344	2025-02-15	2026-02-15	certificado_71722344_262.pdf	\N
265	Cédula	guadid 	benitez diaz	73149593	2025-06-13	2026-06-13	certificado_73149593_265.pdf	\N
268	Cédula	kely	gonzales martinez	100340382	2025-05-20	2026-05-20	certificado_100340382_268.pdf	\N
271	Cédula	ersileidis	beltran salcedo	1001161996	2025-03-12	2026-03-12	certificado_1001161996_271.pdf	\N
275	Cédula	daniel 	montes llana 	1001446575	2025-03-18	2026-03-18	certificado_1001446575_275.pdf	\N
279	Cédula	fabiana 	diaz hernadez 	1005605779	2025-05-20	2026-05-20	certificado_1005605779_279.pdf	\N
282	Cédula	MARIA VALENTINA	FORONDA JARAMILLO	1007567435	2025-01-24	2026-01-24	certificado_1007567435_282.pdf	\N
286	Cédula	JOHANA 	HUERTAS PENAGOS	1017098293	2025-07-07	2026-07-07	certificado_1017098293_286.pdf	\N
290	Cédula	sara lucia 	ochoa graciano 	1017179334	2025-05-20	2026-05-20	certificado_1017179334_290.pdf	\N
293	Cédula	sara yeraldi	restrepo	1020105608	2025-05-21	2026-05-21	certificado_1020105608_293.pdf	\N
296	Cédula	elvira johana 	lopez muñoz	1034557206	2025-05-15	2026-05-15	certificado_1034557206_296.pdf	\N
300	Cédula	DUVER NEY 	MOLINA GIRALDO	1038116593	2025-05-07	2026-05-07	certificado_1038116593_300.pdf	\N
304	Cédula	YAN CARLOS	ARRIETA PEREZ	1039465248	2025-05-08	2026-05-08	certificado_1039465248_304.pdf	\N
307	Cédula	JUAN CAMILO	ARROYO MAZA	1041260627	2025-07-07	2026-07-07	certificado_1041260627_307.pdf	\N
311	Cédula	Sujeidy 	Vanegas Navarro	1051678478	2025-04-14	2026-04-14	certificado_1051678478_311.pdf	\N
314	Cédula	greisy del carmen 	castro ortiz	1063134825	2025-05-07	2026-05-07	certificado_1063134825_314.pdf	\N
318	Cédula	maria daniela	galeano	1070324040	2025-04-04	2026-04-04	certificado_1070324040_318.pdf	\N
325	Cédula	yeimy carolina 	acevedo morales	1097036997	2025-03-18	2026-03-18	certificado_1097036997_325.pdf	\N
342	Cédula	katia del carmen 	hernandez perez	1129566236	2025-05-06	2026-05-06	certificado_1129566236_342.pdf	\N
351	CC	george 	giraldo	12345678	2025-06-05	2026-06-05	certificado_12345678_351.pdf	
337	Cédula	ANAY XIOMARA	TORRES ARIAS 	1123803274	2025-05-08	2026-05-08	certificado_1123803274_337.pdf	\N
347	Cédula	jean duban 	caicedo garcia 	1192770452	2025-04-24	2026-04-24	certificado_1192770452_347.pdf	\N
354	CC	ana	wonka	3456789	2025-08-30	2026-08-30	certificado_3456789_354.pdf	
\.


--
-- Name: certificadosloto_id_documento_seq; Type: SEQUENCE SET; Schema: public; Owner: usuario_loto
--

SELECT pg_catalog.setval('public.certificadosloto_id_documento_seq', 354, true);


--
-- PostgreSQL database dump complete
--

\unrestrict GbO0Y28bo1kapDqf7mNLtOfTDnt1hN8dn1AKxDLJ35OBfBsHCiayXbB7fztWNPn

