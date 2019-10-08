#! /usr/bin/python
# coding: utf8 
import sys
import os
import MySQLdb
import datetime
import time
from datetime import datetime, timedelta
import shutil
import json
import xml.etree.ElementTree as ET
import re
#Retrieve Arg (1 = filename, 2= tabName)
filename = sys.argv[1]
# tabName = sys.argv[2]

#GetGlobalValue (id scan, date import...)
#date 
now = datetime.now()
date_import = now.strftime("%Y-%m-%d")

# Open the workbook and define the worksheet
# book = xlrd.open_workbook(filename)
# sheet = book.sheet_by_name(tabName)

# Establish a MySQL connection
database = MySQLdb.connect (host="XXXXXX", user = "XXXXXX", passwd = "XXXXXXX", db = "XXXXX")

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

tree = ET.parse(filename)
root = tree.getroot()
# print(root.tag)
# conf = root.getchildren()
hostnameTab = []
for hostName in root.findall('fw_policy'):
	hostnameTab.append(hostName.get('name').encode('utf-8').strip())
for hostName in root.findall('fw_sub_policy'):
	hostnameTab.append((hostName.get('name')).encode('utf-8').strip())
	# hostnameTab.append(hostName.get('name').decode('utf8'))
	
print(hostnameTab)

for firewallName in hostnameTab:
	#DATA HISTO
	print ("Historisation des donnees du dernier import stonesoft: " + firewallName)
	try:
		values = ('stonesoft',firewallName)
		query = """INSERT INTO `firewall_flow_matrix_histo`(`id`, `key_rule`, `id_import`, `firewall_name`, `type_fw`, `safe`, `new`, `source`, `dest`, `protocole_port`, `comment`, `action`, `log_level`, `rule_number`, `dest_zone`, `target_zone`, `rule_status`, `obso_counter`, `ref_s2e`) SELECT * FROM `firewall_flow_matrix` WHERE type_fw = %s and firewall_name = %s """
		cursor.execute(query,values)
		# cursor.execute("INSERT INTO `firewall_flow_matrix_histo`(`id`, `key_rule`, `id_import`, `firewall_name`, `type_fw`, `safe`, `new`, `source`, `dest`, `protocole_port`, `comment`, `action`, `log_level`, `rule_number`, `dest_zone`, `target_zone`, `rule_status`, `obso_counter`, `ref_s2e`) SELECT * FROM `firewall_flow_matrix` WHERE type_fw = 'stonesoft' and firewall_name =  %s)
		cursor.close()
		database.commit()	
		print ("Historisation of data succeed") 
	except Exception as e:
		print ('Historisation of Stonesoft '+firewallName+' data FAILED '+str(e))
		sys.exit(1)
	###PURGE DES DONNEES
	cursor = database.cursor()		
	try:
		print ("Debut de la purge...")
		values = ('stonesoft',firewallName)
		query = """DELETE FROM `firewall_flow_matrix` WHERE type_fw = %s and firewall_name = %s """
		cursor.execute(query,values)
		# cursor.execute("DELETE FROM `firewall_flow_matrix` WHERE type_fw = 'stonesoft'")
		cursor.close()
		database.commit()	
		print ("Purge of data succeed")
	except Exception as e:
		print('Purge of firewall_flow_matrix data  '+firewallName+'  FAILED '+str(e))
		cursor.close()
		sys.exit(1)
	
	cursor = database.cursor()
	# Get Imports IDs
	id_import = 0
	values = ('stonesoft',firewallName)
	query = """ select max(id_import) from `firewall_flow_matrix_histo` WHERE type_fw = %s and firewall_name = %s """
	cursor.execute(query,values)
	try:
		results = cursor.fetchone()
		for row in results:
			id_last_batch_tmp = row
			if str(id_last_batch_tmp) == 'None':
				id_last_batch=0
			else:
				id_last_batch = id_last_batch_tmp
	except:
		id_last_batch = 0
	id_import = id_last_batch+1
	# tree = ET.parse(filename)
	# root = tree.getroot()
	# hostnameTab = []
	# for hostName in root.findall('configuration/groups/system/host-name'):
		# hostnameTab.append(hostName.text)
	
	for policies in root.findall('fw_policy'):
		cursor = database.cursor()
		print('Processing '+policies.get('name').encode('utf-8').strip() + ' VS ' +firewallName)
		if (policies.get('name').encode('utf-8').strip() == firewallName):
			# print('GO')
			for policy in policies.findall('access_entry/rule_entry'):
				if policy.find('access_rule') is not None:
					# print('GO')
					rule_number = policy.get('tag')
					comment = policy.get('comment')
					status = policy.get('is_disabled').replace('true','inactive').replace('false','active')
					sourceTmp = '';
					destinationTmp = ''
					protocoleTmp = ''
					
					for src in policy.findall('access_rule/match_part/match_sources/match_source_ref'):
						sourceTmp = sourceTmp + src.get('value')+'---'
					for dest in policy.findall('access_rule/match_part/match_destinations/match_destination_ref'):
						destinationTmp = destinationTmp + dest.get('value')+'---'
					for proto in policy.findall('access_rule/match_part/match_services/match_service_ref') : 
						protocoleTmp = protocoleTmp  + proto.get('value')+'---' 
										
					source=re.sub('---$','',sourceTmp)
					destination=re.sub('---$','',destinationTmp)
					protocole=re.sub('---$','',protocoleTmp)
					key_rule = str(rule_number)+'_'+source+'_'+destination+'_'+protocole
					
					actionTag = policy.find('access_rule/action')
					if actionTag is None:
						action = 'None'
					else:
						action = actionTag.get('type')
					
					log_levelTag = policy.find('access_rule/option/log_policy')
					if log_levelTag is None:
						log_level = 'None'
					else:
						log_level = log_levelTag.get('log_level')

					values = (key_rule,id_import,firewallName,'stonesoft','No','unchanged',source,destination,protocole,comment,action,log_level,rule_number,'','',status,'0','')
					# print(str(values))
					query = """INSERT INTO `firewall_flow_matrix`(`id`,`key_rule`,`id_import`,`firewall_name`, `type_fw`,`safe`,`new`, `source`, `dest`, `protocole_port`, `comment`, `action`, `log_level`, `rule_number`, `dest_zone`, `target_zone`, `rule_status`, `obso_counter`, `ref_s2e` ) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s,%s, %s,%s)"""
					cursor.execute(query,values)																								
					
		# f.close()
		# Close the cursor
		cursor.close()
		# Commit the transaction
		database.commit()
	
	
	for policies in root.findall('fw_sub_policy'):
		cursor = database.cursor()
		print('Processing '+policies.get('name').encode('utf-8').strip() + ' VS ' +firewallName)
		if (policies.get('name').encode('utf-8').strip() == firewallName):
			
			for policy in policies.findall('access_entry/rule_entry'):
				if policy.find('access_rule') is not None:
					# print('GO')
					rule_number = policy.get('tag')
					comment = policy.get('comment')
					status = policy.get('is_disabled').replace('true','inactive').replace('false','active')
					sourceTmp = '';
					destinationTmp = ''
					protocoleTmp = ''
					
					for src in policy.findall('access_rule/match_part/match_sources/match_source_ref'):
						sourceTmp = sourceTmp + src.get('value')+'---'
					for dest in policy.findall('access_rule/match_part/match_destinations/match_destination_ref'):
						destinationTmp = destinationTmp + dest.get('value')+'---'
					for proto in policy.findall('access_rule/match_part/match_services/match_service_ref') : 
						protocoleTmp = protocoleTmp  + proto.get('value')+'---' 
										
					source=re.sub('---$','',sourceTmp)
					destination=re.sub('---$','',destinationTmp)
					protocole=re.sub('---$','',protocoleTmp)
					key_rule = str(rule_number)+'_'+source+'_'+destination+'_'+protocole
					
					actionTag = policy.find('access_rule/action')
					if actionTag is None:
						action = 'None'
					else:
						action = actionTag.get('type')
					
					log_levelTag = policy.find('access_rule/option/log_policy')
					if log_levelTag is None:
						log_level = 'None'
					else:
						log_level = log_levelTag.get('log_level')
			
					values = (key_rule,id_import,firewallName,'stonesoft','No','unchanged',source,destination,protocole,comment,action,log_level,rule_number,'','',status,'0','')
					# print(str(values))
					query = """INSERT INTO `firewall_flow_matrix`(`id`,`key_rule`,`id_import`,`firewall_name`, `type_fw`,`safe`,`new`, `source`, `dest`, `protocole_port`, `comment`, `action`, `log_level`, `rule_number`, `dest_zone`, `target_zone`, `rule_status`, `obso_counter`, `ref_s2e` ) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s,%s, %s,%s)"""
					cursor.execute(query,values)																								
					
	# f.close()
	# Close the cursor
		cursor.close()
	# Commit the transaction
		database.commit()
	##Check des nouvelles rules ou des modifications
	#NEW
	try:
		cursor = database.cursor()
		query = """UPDATE firewall_flow_matrix set new='new' where type_fw = %s and id_import = %s and rule_number not in (select distinct rule_number from firewall_flow_matrix_histo where type_fw = %s and id_import = %s ) """
		values = ('stonesoft',id_import, 'stonesoft' , id_last_batch)
		cursor.execute(query, values)
		database.commit()
		print("CHECK NEW RULES OK " )
	except Exception as e:
		print("Check des nouvelles regles FAILED "+str(e))
		cursor.close()
		# sys.exit(1)
		
	#MODIF
	try:
		cursor = database.cursor()
		query = """UPDATE firewall_flow_matrix set new='modified' where type_fw = %s and id_import = %s and rule_number in (select distinct rule_number from firewall_flow_matrix_histo where type_fw = %s and id_import = %s ) and key_rule not in (select distinct key_rule from firewall_flow_matrix_histo where type_fw = %s and id_import = %s) """
		values = ('stonesoft',id_import, 'stonesoft' , id_last_batch, 'stonesoft' , id_last_batch)
		cursor.execute(query, values)
		database.commit()
		print("CHECK MODIFIED RULES OK " )
	except Exception as e:
		print("Check des modifications sur regles FAILED "+str(e))
		cursor.close()
		sys.exit(1)
		
	##Passage en Await Recertif des besoins ayant des regles modifiees
	try:
		cursor = database.cursor()
		query = """UPDATE flow_approval set validated='Awaiting Recertification' where need_ref in (select idNeed from firewall_needs_flow fnf join firewall_flow_matrix ffm on fnf.key_rule = ffm.key_rule where ffm.new = 'modified')"""
		values = ''
		cursor.execute(query, values)
		database.commit()	
		print("RECERTIFICATION INSERT OK " )		
	except Exception as e:
		print("Update des rules a recertifier FAILED "+str(e))
		cursor.close()
		# sys.exit(1)



##PURGE of OBJEcTS 

cursor = database.cursor()		
try:
	print ("Debut de la purge...")
	values = ()
	query = """DELETE FROM `fw_objects` WHERE 1 """
	cursor.execute(query,values)
	# cursor.execute("DELETE FROM `firewall_flow_matrix` WHERE type_fw = 'stonesoft'")
	cursor.close()
	database.commit()	
	print ("Purge of firewall_objects data succeed")
except Exception as e:
	print('Purge of firewall_objects data FAILED '+str(e))
	cursor.close()
	sys.exit(1)
  
##IMPORT OBJEcTS
try:
	cursor = database.cursor()
	for host in root.findall('host'):
		name = host.get('name')
		value = host.find('mvia_address').get('value')
		
		value2Tmp = ''	
		for secondary in host.findall('secondary'):
			value2Tmp = value2Tmp + secondary.get('value')+'---'
		value2=re.sub('---$','',value2Tmp)
		
		values = (name , value , value2)
		query = """INSERT INTO `fw_objects` (`id`, `name`, `value1`, `value2`) VALUES (NULL , %s, %s, %s) """
		cursor.execute(query,values)	
		
	database.commit()
	database.close()
	print("FW OBJECT INSERTION OK ")
except Exception as e:
		print("FW OBJECT INSERTION FAILED "+str(e))
		cursor.close()

# Print results
print ""
print "All Done!"
print ""
