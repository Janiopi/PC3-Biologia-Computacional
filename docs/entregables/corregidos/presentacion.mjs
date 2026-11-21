import fs from 'node:fs/promises';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const root='/home/janiopi/Downloads/Dengue';
const dest=root+'/docs/entregables/corregidos';
const data=JSON.parse(await fs.readFile(dest+'/contenido_presentacion.json','utf8'));
const p=Presentation.create({slideSize:{width:1280,height:720}});
for(const [i,item] of data.entries()){
 const s=p.slides.add();s.background.fill='#FFFFFF';
 function text(value,x,y,w,h,size,color='#173448'){
  const box=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  box.text=value;box.text.style={fontFamily:'DejaVu Sans',fontSize:size,color};return box;
 }
 text(item.title,55,35,1170,95,36);
 text(item.body,55,140,1170,item.chart?200:500,item.chart?22:25);
 if(i===2 || i===3){
 const labels=i===2?['Ih','Ev','Iv','Eh','Ih']:['Sh','Eh','Ih','Rh'];
 labels.forEach((label,j)=>{const x=80+j*230;const box=s.shapes.add({geometry:'rect',position:{left:x,top:430,width:145,height:70},fill:'#EAF3F4',line:{fill:'#207D8D',width:2}});box.text=label;box.text.style={fontFamily:'DejaVu Sans',fontSize:30,color:'#173448'};if(j<labels.length-1)text('→',x+155,440,65,60,35);});
 text(i===2?'Transmisión (+) e incubación (+). Recuperación y agotamiento de susceptibles compensan.':'Ch: contador independiente con entrada σh Eh. Vector: Sv → Ev → Iv, con muertes por nivel.',80,535,1120,100,24);
 }
 if(item.chart)s.charts.add('bar',{position:{left:65,top:350,width:1150,height:285},categories:item.chart.categories,series:[{name:'PRCC',values:item.chart.values,fill:'#207D8D'}],hasLegend:false,yAxis:{numberFormatCode:'0.00'},dataLabels:{showValue:true,position:'outEnd',numberFormatCode:'0.00'}});
 text(`${i+1} / 16 · Dengue LHS/PRCC · Resultados regenerados`,55,674,1100,25,14,'#52616B');
}
await (await PresentationFile.exportPptx(p)).save(root+'/work/mejora_20261120/build/candidato.pptx');
for(const [i,s] of p.slides.items.entries()){
 const png=await p.export({slide:s,format:'png',scale:0.7});await fs.writeFile(root+`/work/mejora_20261120/build/slide-${i+1}.png`,new Uint8Array(await png.arrayBuffer()));
}
const skill='/home/janiopi/.codex/plugins/cache/openai-primary-runtime/presentations/26.1015.12040/skills/presentations';
const {finalizePresentation}=await import(skill+'/container_tools/artifact_tool_utils.mjs');
await finalizePresentation({workspaceDir:root,candidatePath:root+'/work/mejora_20261120/build/candidato.pptx',finalPath:dest+'/Dengue_LHS_PRCC_corregido.pptx',pythonExecutable:'/home/janiopi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python',integrityValidatorPath:skill+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:skill+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000'],materializeLiteralChartWorkbooks:true,requiredNativeChartOwnerSlides:[11,12,13],fontPolicy:{basis:'design',families:['DejaVu Sans','Aptos']},verifyArtifactToolImport:true,receiptPath:root+'/work/mejora_20261120/build/validacion.json'});
