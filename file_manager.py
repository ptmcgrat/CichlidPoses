import platform, os, pdb, subprocess
import pandas as pd

class FileManager():
	def __init__(self, rcloneRemote = 'ptm_dropbox:/', masterDir = 'COS/BioSci/BioSci-McGrath/Apps/CichlidMorphometricData/'):
		
		# Set master directories/remotes
		if platform.node() == 'ebb-utaka.biosci.gatech.edu' or platform.node() == 'utaka.biosci.gatech.edu' or 'utaka' in platform.node():
			self.localMasterDir = '/Data/' + os.getenv('USER') + '/Temp/CichlidMorphometricData/'
		else:
			self.localMasterDir = os.getenv('HOME').rstrip('/') + '/' + 'Temp/CichlidMorphometricData/' #Master directory for local data
		
		self.rcloneRemote = rcloneRemote
		self.cloudMasterDir = self.rcloneRemote + masterDir
	
		# Create file structure for data
		self._createMasterDirs()

	def _createMasterDirs(self):

		self.localAnnotationsDir = self.localMasterDir + '__AnnotatedData/'	
		self.localMLMDir = self.localMasterDir + '__MachineLearningModels/'		
		self.localProjectDir = self.localMasterDir + '__ProjectData/'

	def downloadData(self, local_data, tarred = False, tarred_subdirs = False, parallel = False, rclone=False):

		relative_name = local_data.rstrip('/').split('/')[-1] + '.tar' if tarred else local_data.rstrip('/').split('/')[-1]
		local_path = local_data.split(local_data.rstrip('/').split('/')[-1])[0]
		cloud_path = local_path.replace(self.localMasterDir, self.cloudMasterDir)

		cloud_objects = subprocess.run(['rclone', 'lsf', cloud_path], capture_output = True, encoding = 'utf-8').stdout.split()

		if relative_name + '/' in cloud_objects: #directory
			output = subprocess.run(['rclone', 'copy', cloud_path + relative_name, local_path + relative_name], capture_output = True, encoding = 'utf-8')
		elif relative_name in cloud_objects: #file
			if parallel:
				process = subprocess.Popen(['rclone', 'copy', cloud_path + relative_name, local_path])
				return process
			elif rclone:
				output = subprocess.run(['rclone', 'copy', '--multi-thread-streams', '96', '--multi-thread-cutoff','100Mi', cloud_path + relative_name, local_path], capture_output = True, encoding = 'utf-8')
			else:
				output = subprocess.run(['rclone', 'copy', cloud_path + relative_name, local_path], capture_output = True, encoding = 'utf-8')

		else:
			raise FileNotFoundError('Cant find file for download: ' + cloud_path + relative_name)

		if not os.path.exists(local_path + relative_name):
			raise FileNotFoundError('Error downloading: ' + local_path + relative_name)

		if tarred:
			# Untar directory
			output = subprocess.run(['tar', '-xvf', local_path + relative_name, '-C', local_path], capture_output = True, encoding = 'utf-8')
			output = subprocess.run(['rm', '-f', local_path + relative_name], capture_output = True, encoding = 'utf-8')

		if tarred_subdirs:
			for d in [x for x in os.listdir(local_data) if '.tar' in x]:
				output = subprocess.run(['tar', '-xvf', local_data + d, '-C', local_data, '--strip-components', '1'], capture_output = True, encoding = 'utf-8')
				os.remove(local_data + d)

	def uploadData(self, local_data, tarred = False, parallel = False):

		relative_name = local_data.rstrip('/').split('/')[-1]
		local_path = local_data.split(relative_name)[0]
		cloud_path = local_path.replace(self.localMasterDir, self.cloudMasterDir)

		if tarred:
			output = subprocess.run(['tar', '-cvf', local_path + relative_name + '.tar', '-C', local_path, relative_name], capture_output = True, encoding = 'utf-8')
			if output.returncode != 0:
				if '.DS_Store' not in output.stderr:
					print(output.stderr)
					raise Exception('Error in tarring ' + local_data)
			relative_name += '.tar'

		if os.path.isdir(local_path + relative_name):
			if parallel:
				command = ['rclone', 'copy', local_path + relative_name, cloud_path + relative_name]
				return command
			else:
				output = subprocess.run(['rclone', 'copy', local_path + relative_name, cloud_path + relative_name], capture_output = True, encoding = 'utf-8')
			#subprocess.run(['rclone', 'check', local_path + relative_name, cloud_path + relative_name], check = True)

		elif os.path.isfile(local_path + relative_name):
			#print(['rclone', 'copy', local_path + relative_name, cloud_path])
			if parallel:
				command = ['rclone', 'copy', local_path + relative_name, cloud_path]
				return command
			else:
				output = subprocess.run(['rclone', 'copy', local_path + relative_name, cloud_path], capture_output = True, encoding = 'utf-8')
				output = subprocess.run(['rclone', 'check', local_path + relative_name, cloud_path], check = True, capture_output = True, encoding = 'utf-8')
		else:
			raise Exception(local_data + ' does not exist for upload')

		if not parallel:
			if output.returncode != 0:
				if '.DS_Store' not in output.stderr:
					raise Exception('Error in uploading file: ' + output.stderr)

	def returnFileSize(self, local_data):
		output = subprocess.run(['rclone', 'size', local_data.replace(self.localMasterDir, self.cloudMasterDir)], capture_output = True, encoding = 'utf-8')
		return int(output.stdout.split(' Byte)')[0].split('(')[-1])

	def returnCloudDirs(self, local_data):
		output = subprocess.run(['rclone', 'lsf', local_data.replace(self.localMasterDir, self.cloudMasterDir)], capture_output = True, encoding = 'utf-8')
		return [x.rstrip('/') for x in output.stdout.split('\n') if x.endswith('/') ]

	def returnCloudFiles(self, local_data):
		output = subprocess.run(['rclone', 'lsf', local_data.replace(self.localMasterDir, self.cloudMasterDir)], capture_output = True, encoding = 'utf-8')
		return [x.rstrip('/') for x in output.stdout.split('\n') if not x.endswith('/') ]

	def checkCloudFile(self, local_data):

		relative_name = local_data.rstrip('/').split('/')[-1]
		local_path = local_data.split(relative_name)[0]
		cloud_path = local_path.replace(self.localMasterDir, self.cloudMasterDir)

		uploadedFiles = self.returnCloudFiles(local_path)

		if relative_name in uploadedFiles:
			return True 
		else:
			return False







