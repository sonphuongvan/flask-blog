pipeline{

	agent any
	
    options {
        buildDiscarder logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '10', daysToKeepStr: '', numToKeepStr: '10')
    }
    
	environment {
		DOCKERHUB_CREDENTIALS=credentials('dockerhub')
		GOOGLE_CHAT_URL='https://chat.googleapis.com/v1/spaces/AAAAWtbf8PM/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=1HTJUa1tltyjBx236x6VGTpKy1J0d05hzlnIwgaBuFc%3D'
		def BUILDVERSION = sh(script: "echo `date +%s`", returnStdout: true).trim()
	}

	stages {
	    stage('gitclone') {
			steps {
				sh 'git clone git@github.com:sonphuongvan/flask-blog.git'
			}
            post {
				success {
				   sendSucessNotification()
		        }
		        failure {
		           sendFailNotification()
		        }
			}
		}

		stage('Build') {
			steps {
			    sh 'docker build -t phuongsonkma/flask-blog:${BUILDVERSION} /home/jenkins/workspace/flask-blog/flask-blog/ --cache-from phuongsonkma/flask-blog:latest'
			    sh 'docker tag phuongsonkma/flask-blog:${BUILDVERSION} phuongsonkma/flask-blog:latest'
			}
            post {
				success {
				   sendSucessNotification()
				}
		        failure {
		           sendFailNotification()
		        }
			}
		}
		
		stage('Scan'){
		    steps {
                script {
                    catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {
                        def VULN_CHECK = sh(script: 'docker scan --severity=high phuongsonkma/flask-blog:latest ; exit 0', returnStatus: true)
                        if ( VULN_CHECK == 1 ) {
                            slackSend channel: '#jenkins',  color: 'danger', message: "There have a vulnerability in this project!"
                            googlechatnotification url: "${GOOGLE_CHAT_URL}", message: 'There have a vulnerability in this project!', notifyAborted: 'true', notifyFailure: 'true', notifyNotBuilt: 'true', notifySuccess: 'true', notifyUnstable: 'true', notifyBackToNormal: 'true', suppressInfoLoggers: 'true', sameThreadNotification: 'true'
                        }  else {
                            slackSend channel: '#jenkins',  color: 'good', message: "Your app is OK!"
                        }
                    }
                }
		    }
            post {
				success {
				   sendSucessNotification()
		        }
		        failure {
		           sendFailNotification()
		        }
			}
		}

		stage('Push') {
			steps {
			    sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
			    sh 'docker push phuongsonkma/flask-blog:${BUILDVERSION}'
				sh 'docker push phuongsonkma/flask-blog:latest'
			}
            post {
				success {
				   sendSucessNotification()
		        }
		        failure {
		           sendFailNotification()
		        }
			}
		}
		
		stage("Deploy"){
		    steps {
                sh "ssh -tt jenkins@172.16.10.12 'docker pull phuongsonkma/flask-blog:latest'"
                sh "ssh -tt jenkins@172.16.10.12 'docker stop flask-blog'"
                sh "ssh -tt jenkins@172.16.10.12 'docker rm flask-blog'"
                sh "ssh -tt jenkins@172.16.10.12 'docker run -dp 5000:5000 --name=flask-blog phuongsonkma/flask-blog:latest'"
                sh "ssh -tt jenkins@172.16.10.12 'docker image prune -af'"
            }
            post {
				success {
				   sendSucessNotification()
		        }
		        failure {
		           sendFailNotification()
		        }
			}
		}
	}

	post {
		always {
			sh 'docker logout'
			sh 'rm -rf /home/jenkins/workspace/flask-blog/flask-blog'
			sh "ssh -tt jenkins@172.16.10.12 'docker image prune -af'"
			sh 'docker image prune -a --force --filter "until=240h"'
		}
		success {
		   sendSucessNotification()
        }
        failure {
           sendFailNotification()
        }
	}
	
}

def sendSucessNotification(){
    slackSend (color: 'good', message: """SUCCESS: Job "${env.STAGE_NAME} ${env.JOB_NAME} [${env.BUILD_NUMBER}]" """)
	googlechatnotification url: "${GOOGLE_CHAT_URL}", message: "SUCCESS: job ${env.STAGE_NAME}", notifyAborted: 'true', notifyFailure: 'true', notifyNotBuilt: 'true', notifySuccess: 'true', notifyUnstable: 'true', notifyBackToNormal: 'true', suppressInfoLoggers: 'true', sameThreadNotification: 'true'
}

def sendFailNotification(){
    slackSend (color: 'danger', message: """FAIL: Job "${env.STAGE_NAME} ${env.JOB_NAME} [${env.BUILD_NUMBER}]" """)
	googlechatnotification url:"${GOOGLE_CHAT_URL}", message: "FAIL: job ${env.STAGE_NAME}", notifyAborted: 'true', notifyFailure: 'true', notifyNotBuilt: 'true', notifySuccess: 'true', notifyUnstable: 'true', notifyBackToNormal: 'true', suppressInfoLoggers: 'true', sameThreadNotification: 'true'
}
