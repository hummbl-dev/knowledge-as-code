#!/usr/bin/env python3
import copy,json,sys
from pathlib import Path
from urllib.parse import urlparse
OPS=('discover','resolve','retrieve','snapshot','normalize','verify','cite','refresh','delete_or_invalidate')
FAIL={'not_found','ambiguous','unauthorized','rate_limited','unsupported','restricted','stale','superseded','checksum_mismatch','malformed_upstream','deleted','transient_failure','policy_blocked'}
PATTERNS={
 'scholarly_api':dict(adapter='scholarly-api-fixture',source='crossref',family='scholarly_literature',plane='public',modes=['api_retrieval'],auth='optional',snapshot='external_reference_only',locator='doi',version='mutable_with_version',checksum='conditional'),
 'versioned_repository':dict(adapter='repository-fixture',source='github',family='software_and_packages',plane='mixed',modes=['api_retrieval','connector_retrieval'],auth='varies',snapshot='bounded_snapshot_permitted',locator='commit_path_lines',version='immutable',checksum='available'),
 'archive_item':dict(adapter='archive-fixture',source='internet-archive',family='web_and_archives',plane='public',modes=['api_retrieval','bounded_bulk_snapshot'],auth='optional',snapshot='bounded_snapshot_permitted',locator='archive_page',version='immutable',checksum='conditional'),
 'multimedia_item':dict(adapter='multimedia-fixture',source='youtube',family='multimedia',plane='public',modes=['api_retrieval','live_retrieval'],auth='required',snapshot='external_reference_only',locator='media_timestamp',version='mutable_with_version',checksum='unavailable'),
 'private_connector':dict(adapter='private-connector-fixture',source='private-connector-fixture',family='authorized_private_sources',plane='authorized_private',modes=['connector_retrieval'],auth='required',snapshot='connector_reference_only',locator='connector_object_id',version='mutable_with_version',checksum='unavailable')}
def https(v):
 try:return isinstance(v,str) and urlparse(v).scheme=='https' and bool(urlparse(v).netloc)
 except:return False
def operations(private=False):
 out={op:{'support':'supported','completeness':'complete_possible','notes':'Fixture behavior only.'} for op in OPS}
 out['delete_or_invalidate']={'support':'restricted','completeness':'conditional','notes':'Invalidation is represented; upstream deletion is source-governed.'}
 if private:
  out['discover']={'support':'authorization_gated','completeness':'conditional','notes':'Requires authorization.'}
  out['retrieve']={'support':'authorization_gated','completeness':'conditional','notes':'Requires authorization.'}
  out['snapshot']={'support':'restricted','completeness':'not_applicable','notes':'Persistent copy is not permitted by this fixture.'}
 return out
def build(name):
 p=PATTERNS[name];private=p['plane']=='authorized_private';checksum=None if p['checksum']=='unavailable' else {'algorithm':'sha256','value':'0'*64}
 manifest={'schema_version':'adapter_manifest.v0.1','adapter_id':p['adapter'],'source_id':p['source'],'source_family':p['family'],'data_plane':p['plane'],'access_modes':p['modes'],'authentication':p['auth'],'snapshot_policy':p['snapshot'],'operations':operations(private),'exact_locator_support':[p['locator']],'version_support':p['version'],'checksum_support':p['checksum'],'known_limitations':['Fixture-only; no live provider conformance is claimed.'],'conformance_status':'fixture_candidate'}
 result={'schema_version':'adapter_result.v0.1','result_id':p['adapter']+'.result-001','adapter_id':p['adapter'],'source_id':p['source'],'operation':'retrieve','status':'success','completeness':'complete','canonical_uri':'https://example.invalid/item','source_identifier':{'system':'fixture_id','value':'item-001'},'source_version':'fixture-v1','retrieved_at':'2026-07-11T23:45:00Z','content_type':'application/json','privacy_class':'authorized_private' if private else 'public','license_posture_ref':'source-registry:fixture','acquisition_method':'connector_retrieval' if private else 'fixture','record_state':'current','integrity_status':'checksum_unavailable' if checksum is None else 'verified','checksum':checksum,'exact_locator':{'type':p['locator'],'value':'item-001'},'transformations':[],'parent_artifact_ids':[],'errors':[]}
 case={'case_id':'fixture-case-001','operation':'retrieve','expected_status':'success','observed_status':'success','passed':True,'notes':'Deterministic fixture.'}
 receipt={'schema_version':'adapter_conformance_receipt.v0.1','receipt_id':p['adapter']+'.receipt-001','adapter_id':p['adapter'],'source_id':p['source'],'fixture_version':'v0.1','executed_at':'2026-07-11T23:46:00Z','fact_posture':'local_execution','environment':{'runtime':'python','runtime_version':sys.version.split()[0]},'commands':['python3 scripts/validate_adapter_contract.py --self-test fixtures/adapters/adapter-contract-v0.1.fixtures.json'],'cases':[case],'summary':{'total':1,'passed':1,'failed':0},'limitations':['No live provider behavior was tested.'],'promotion_disposition':'fixture_candidate'}
 return {'schema_version':'adapter_fixture_packet.v0.1','manifest':manifest,'result':result,'receipt':receipt}
def mutate(packet,kind):
 p=copy.deepcopy(packet);m=p['manifest'];r=p['result'];rc=p['receipt']
 if kind=='partial_as_complete':r['status']='partial';r['completeness']='complete'
 elif kind=='unsupported_success':m['operations']['retrieve']={'support':'unsupported','completeness':'not_applicable','notes':'Unsupported.'}
 elif kind=='rate_limit_as_success':r['errors']=[{'code':'rate_limited','message':'Fixture rate limit.'}]
 elif kind=='stale_as_current':r['record_state']='stale'
 elif kind=='checksum_mismatch_as_success':r['integrity_status']='checksum_mismatch'
 elif kind=='private_public_confusion':r['privacy_class']='public'
 elif kind=='live_validation_without_receipt':m['conformance_status']='live_validated';m.pop('conformance_receipt',None)
 elif kind=='receipt_summary_mismatch':rc['summary']={'total':2,'passed':2,'failed':0}
 else:raise ValueError(kind)
 return p
def manifest(m):
 e=[]
 if m.get('schema_version')!='adapter_manifest.v0.1':e.append('manifest schema invalid')
 for op in OPS:
  c=(m.get('operations') or {}).get(op)
  if not c:e.append(f'manifest missing operation {op}')
  elif c.get('support')=='unsupported' and c.get('completeness')!='not_applicable':e.append(f'{op} unsupported must be not_applicable')
 if m.get('data_plane')=='authorized_private' and 'connector_retrieval' not in m.get('access_modes',[]):e.append('private adapter requires connector_retrieval')
 if m.get('data_plane')=='public' and m.get('snapshot_policy')=='connector_reference_only':e.append('public adapter cannot use connector_reference_only')
 if m.get('conformance_status') in {'fixture_validated','live_validated'} and not https(m.get('conformance_receipt')):e.append('validated adapter requires receipt URI')
 return e
def result(r,m):
 e=[]
 if r.get('schema_version')!='adapter_result.v0.1':e.append('result schema invalid')
 if not https(r.get('canonical_uri')):e.append('result canonical URI invalid')
 s=r.get('status');c=r.get('completeness')
 if s=='partial' and c!='partial':e.append('partial status requires partial completeness')
 if s in FAIL and c!='none':e.append('failure status requires none completeness')
 if s=='success' and c not in {'complete','partial'}:e.append('success completeness invalid')
 if s in {'success','partial'} and not isinstance(r.get('exact_locator'),dict):e.append('successful result requires exact locator')
 if s=='success' and r.get('errors'):e.append('success cannot contain errors')
 if r.get('record_state') in {'stale','superseded','deleted'} and s=='success':e.append('non-current record reported as success')
 if r.get('integrity_status')=='checksum_mismatch' and s!='checksum_mismatch':e.append('checksum mismatch reported as success')
 if r.get('integrity_status')=='verified' and not isinstance(r.get('checksum'),dict):e.append('verified integrity requires checksum')
 if r.get('adapter_id')!=m.get('adapter_id') or r.get('source_id')!=m.get('source_id'):e.append('result identity mismatch')
 if (m.get('operations') or {}).get(r.get('operation'),{}).get('support')=='unsupported' and s in {'success','partial'}:e.append('unsupported operation succeeded')
 if m.get('data_plane')=='authorized_private' and r.get('privacy_class')!='authorized_private':e.append('private posture lost')
 return e
def receipt(rc,m):
 e=[]
 if rc.get('schema_version')!='adapter_conformance_receipt.v0.1':e.append('receipt schema invalid')
 if rc.get('fact_posture')!='local_execution':e.append('receipt fact posture invalid')
 if not isinstance(rc.get('limitations'),list) or not rc.get('limitations'):e.append('receipt limitations required')
 if rc.get('promotion_disposition') not in {'fixture_candidate','fixture_validated','live_validated','restricted','quarantined','rejected'}:e.append('receipt promotion disposition invalid')
 cases=rc.get('cases') or [];summary=rc.get('summary') or {};passed=sum(x.get('passed') is True for x in cases);failed=len(cases)-passed
 if summary!={'total':len(cases),'passed':passed,'failed':failed}:e.append('receipt summary mismatch')
 if any(x.get('expected_status')!=x.get('observed_status') or x.get('passed') is not True for x in cases):e.append('receipt case mismatch')
 if rc.get('adapter_id')!=m.get('adapter_id') or rc.get('source_id')!=m.get('source_id'):e.append('receipt identity mismatch')
 return e
def validate(p):
 if p.get('schema_version')!='adapter_fixture_packet.v0.1':return['packet schema invalid']
 m=p.get('manifest') or {};return manifest(m)+result(p.get('result') or {},m)+receipt(p.get('receipt') or {},m)
def main(a):
 if a[:1]!=['--self-test'] or len(a)!=2:print('usage: validate_adapter_contract.py --self-test <fixtures.json>',file=sys.stderr);return 2
 spec=json.loads(Path(a[1]).read_text());fail=0
 for name in spec['valid']:
  e=validate(build(name));print(('PASS' if not e else 'FAIL')+' valid:'+name);fail+=bool(e)
  if e:print(e,file=sys.stderr)
 for x in spec['invalid']:
  e=validate(mutate(build(x['base']),x['mutation']));print(('PASS' if e else 'FAIL')+' invalid rejected:'+x['name']);fail+=not bool(e)
 return 1 if fail else 0
if __name__=='__main__':raise SystemExit(main(sys.argv[1:]))
