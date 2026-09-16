import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const root=path.resolve('.');
const skill=process.env.CODEX_PRESENTATIONS_SKILL_DIR;
const py=process.env.CODEX_BUNDLED_PYTHON;
if(!skill || !py) throw new Error('Define CODEX_PRESENTATIONS_SKILL_DIR y CODEX_BUNDLED_PYTHON con las rutas del equipo actual.');
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
await fs.mkdir(path.join(root,'build'),{recursive:true});
const m=JSON.parse(await fs.readFile('artifacts/metricas.json','utf8'));
const c=JSON.parse(await fs.readFile('artifacts/carga.json','utf8'));
const p=Presentation.create({slideSize:{width:1280,height:720}});
function txt(s,text,x,y,w,h,size=29,color='#173345',bold=false){
 const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=text;sh.text.style={typeface:'Calibri',fontSize:size,color,bold,autoFit:'none'};return sh;
}
function slide(title,note=''){
 const s=p.slides.add();s.background.fill='#F5F7F8';
 txt(s,title,65,45,1140,110,44,'#123B50',true);
 txt(s,`NexaFlow     EPE 3     ${p.slides.items.length}`,65,665,1140,30,19,'#506571');
 s.speakerNotes.textFrame.setText(note);return s;
}
let s=slide('NexaFlow\nPredicción de demanda','Completar nombre, sección, docente y fecha. Presentación de trabajo basada en el prototipo local.');
txt(s,'Prototipo web con Machine Learning',65,220,1100,80,38);
txt(s,'Demostración académica con datos sintéticos',65,350,1100,65,30,'#006B68',true);
txt(s,'Estudiante y sección: completar antes de entregar',65,510,1100,60,25);
s=slide('Problema y alcance','Fuente del caso: mensaje del estudiante. Verificar continuidad con EPE 2. No existen mediciones de ahorro o quiebres de stock.');
txt(s,'Decisión que apoya',65,185,470,50,31,'#006B68',true);
txt(s,'Revisar la reposición a partir de la demanda estimada para una zona y un día.',65,255,500,230,33);
txt(s,'Alcance del prototipo',685,185,500,50,31,'#006B68',true);
txt(s,'Cuatro zonas\nDemanda agregada diaria\nCinco variables de entrada\nRevisión humana del resultado',685,255,510,280,31);
s=slide('Integración de la aplicación','Implementación: app.py, api.py y train_model.py. Flask consume FastAPI por HTTP. Documentación: https://fastapi.tiangolo.com/tutorial/body/ y https://flask.palletsprojects.com/en/stable/quickstart/.');
txt(s,'01  Interfaz Flask',65,180,560,60,33,'#006B68',true);
txt(s,'Formulario y mensajes de resultado\nPuerto 5000',65,245,530,120,29);
txt(s,'02  API FastAPI',690,180,520,60,33,'#006B68',true);
txt(s,'Validación y consulta del modelo\nPuerto 8000',690,245,520,120,29);
txt(s,'03  Modelo Scikit-learn',65,430,1100,60,33,'#006B68',true);
txt(s,'Entrenamiento previo y carga del modelo al iniciar el servicio',65,500,1110,100,29);
s=slide('Datos y evaluación temporal','Fuente: artifacts/metricas.json y train_model.py. Referencia metodológica: https://scikit-learn.org/stable/modules/cross_validation.html. El rezago observado se actualiza para cada predicción diaria.');
txt(s,'2.896 registros sintéticos',65,175,1100,65,39,'#006B68',true);
txt(s,'2023–2024, cuatro zonas y semilla 42',65,260,1100,55,30);
txt(s,'2.316 filas para desarrollo con cinco ventanas temporales\n580 filas reservadas para prueba desde el 09-08-2024',65,360,1130,130,30);
txt(s,'Selección por MAE entre regresión lineal y cuatro configuraciones Random Forest',65,535,1100,85,28);
s=slide('Aplicación en funcionamiento','Captura real de artifacts/interfaz_resumen.png. Ejemplo: zona 1, sábado 19 de septiembre de 2026, promoción 1 y rezago 95.0. Datos sintéticos.');
s.images.add({blob:new Uint8Array(await fs.readFile('artifacts/interfaz_resumen.png')),contentType:'image/png',alt:'Formulario y resultado real de NexaFlow con predicción de 113,7 unidades',fit:'contain',position:{left:50,top:160,width:770,height:480}});
txt(s,'113,7 ± 8,1 unidades',845,220,370,115,35,'#006B68',true);
txt(s,'Escenario sintético\nRMSE de test: referencia de error, no intervalo de confianza.\n\nLa recomendación compara con el promedio reciente de la ruta.',845,345,360,250,24);
s=slide('Error en el período de prueba','Fuente: artifacts/metricas.json, test_metricas y baseline_lag7_test. MAE y RMSE en unidades. Comparación sobre las mismas 580 filas. Menor valor es mejor.');
const chart=s.charts.add('bar',{position:{left:65,top:170,width:760,height:430},categories:['MAE','RMSE'],series:[{name:'Regresión lineal',values:[+m.test_metricas.MAE.toFixed(2),+m.test_metricas.RMSE.toFixed(2)],fill:'#006B68'},{name:'Persistencia semanal',values:[+m.baseline_lag7_test.MAE.toFixed(2),+m.baseline_lag7_test.RMSE.toFixed(2)],fill:'#A2AFB7'}],barOptions:{direction:'column',grouping:'clustered'},hasLegend:true,dataLabels:{showValue:false}});
applyPresentationChartFont(chart,{fontFamily:'Calibri'});
txt(s,`MAE  ${m.test_metricas.MAE.toFixed(2)}\nRMSE  ${m.test_metricas.RMSE.toFixed(2)}\nR²  ${m.test_metricas.R2.toFixed(3)}`,890,220,315,220,34,'#006B68',true);
txt(s,'Datos sintéticos\nMenor error no implica ahorro empresarial demostrado.',890,475,315,140,26);
s=slide('Documentación y prueba de la API','Captura de /docs del servicio FastAPI en ejecución local. La documentación es autónoma y /openapi.json conserva el esquema generado por FastAPI.');
s.images.add({blob:new Uint8Array(await fs.readFile('artifacts/api_docs.png')),contentType:'image/png',alt:'Documentación interactiva de FastAPI con prueba de POST /predict y respuesta HTTP 200',fit:'contain',position:{left:65,top:155,width:635,height:480}});
txt(s,'/docs',750,205,400,80,43,'#006B68',true);
txt(s,'Prueba interactiva de POST /predict\n\nValidación de entradas: 422\nModelo no disponible: 503\nEsquema: /openapi.json',750,315,420,300,27);
s=slide('Pruebas y carga local','Fuentes: test_app.py, salida actual de pytest y artifacts/carga.json. 100 solicitudes con concurrencia 10 por flujo y una petición previa de calentamiento. Windows local.');
txt(s,'22 pruebas aprobadas',65,180,1100,80,44,'#006B68',true);
txt(s,'Predicciones, entradas inválidas, integración y fallos del servicio',65,280,1100,90,29);
txt(s,`API: p95 ${c.api.p95_ms.toFixed(1)} ms\nWeb y API: p95 ${c.web.p95_ms.toFixed(1)} ms\n0 errores en ambos escenarios`,65,400,700,190,32);
txt(s,'100 solicitudes\n10 concurrentes\npor escenario',870,415,330,170,30);
s=slide('Validación pendiente','La usabilidad humana no se ha ejecutado. Protocolo completo en PLAN_DE_TRABAJO.md. No se dispone de datos operacionales autorizados.');
txt(s,'Datos empresariales',65,180,550,70,34,'#006B68',true);
txt(s,'Verificar origen y calidad.\nReentrenar y evaluar errores por zona y costos operativos.',65,280,530,240,31);
txt(s,'Usabilidad con participantes',685,180,520,90,34,'#006B68',true);
txt(s,'Realizar tareas con 3–5 personas.\nRegistrar éxito, tiempo y dificultades.\nCorregir y volver a probar.',685,300,530,270,30);
s=slide('Entregables y cierre','Fuente de requisitos: P_ACTIVIDAD_2024 VF.pdf, actividad evaluativa IPCHILE. Repositorio: https://github.com/RenatoLV/EPE3-IPCHILE-ING. Verificar acceso del docente y el mismo commit.');
txt(s,'Informe Word y PDF con desarrollo y evidencias',65,190,1100,95,33);
txt(s,'Código, modelo, pruebas y evidencia de ejecución',65,330,1100,80,33);
txt(s,'Repositorio: github.com/RenatoLV/EPE3-IPCHILE-ING\nPendiente: datos personales y prueba con usuarios reales',65,470,1100,120,31,'#006B68',true);
await (await PresentationFile.exportPptx(p)).save('build/candidate.pptx');
await finalizePresentation({workspaceDir:root,candidatePath:path.join(root,'build/candidate.pptx'),finalPath:path.join(root,'entregables/Presentacion_EPE3_regenerada.pptx'),pythonExecutable:py,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],fontPolicy:{basis:'design',families:['Calibri']},requiredNativeChartOwnerSlides:[6],materializeLiteralChartWorkbooks:true,verifyArtifactToolImport:true,receiptPath:path.join(root,'build/deck-validation-regenerada.json')});
for(let i=0;i<p.slides.items.length;i++){
 const png=await p.export({slide:p.slides.items[i],format:'png',scale:1});
 await fs.writeFile(`build/slide-${i+1}.png`,new Uint8Array(await png.arrayBuffer()));
}
console.log('PPTX finalizado');



