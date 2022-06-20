pipeline{

	agent any
	
    options {
        buildDiscarder logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '10', daysToKeepStr: '', numToKeepStr: '10')
    }
    
	environment {
		DOCKERHUB_CREDENTIALS=credentials('dockerhub')
	}

	stages {
	    stage('gitclone') {
			steps {
				sh 'git clone git@github.com:sonphuongvan/flask-blog.git'
				sh 'pwd'
			}
            post {
				success {
				   slackSend (color: 'good', message: """SUCCESS: Job "${env.STAGE_NAME} ${env.JOB_NAME} [${env.BUILD_NUMBER}]" """)
		        }
		        failure {
		           slackSend (color: 'danger', message: """FAIL: Job "${env.STAGE_NAME} ${env.JOB_NAME} [${env.BUILD_NUMBER}]" """)
		        }
			}
		}

		stage('Build') {
			steps {
			    sh 'docker build -t phuongsonkma/flask-blog:latest /home/jenkins/workspace/flask-blog/flask-blog/'
			}
            post {
				success {
				   slackSend (color: 'good', message: """SUCCESS: Job "${env.STAGE_NAME} ${env.JOB_NAME} [${env.BUILD_NUMBER}]" """)
		        }
		        failure {
		           slackSend (color: 'danger', message: """FAIL: Job "${env.STAGE_NAME} ${env.JOB_NAME} [${env.BUILD_NUMBER}]" """)
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
                        }  else {
                            slackSend channel: '#jenkins',  color: 'good', message: "Your app is OK!"
                        }
                    }
                }
		    }
            post {
				success {
				   slackSend (color: 'good', message: """SUCCESS: Job "${env.STAGE_NAME} ${env.JOB_NAME} [${env.BUILD_NUMBER}]" """)
		        }
		        failure {
		           slackSend (color: 'danger', message: """FAIL: Job "${env.STAGE_NAME} ${env.JOB_NAME} [${env.BUILD_NUMBER}]" """)
		        }
			}
		}

		stage('Push') {
			steps {
			    sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
				sh 'docker push phuongsonkma/flask-blog:latest'
			}
            post {
				success {
				   slackSend (color: 'good', message: """SUCCESS: Job "${env.STAGE_NAME} ${env.JOB_NAME} [${env.BUILD_NUMBER}]" """)
		        }
		        failure {
		           slackSend (color: 'danger', message: """FAIL: Job "${env.STAGE_NAME} ${env.JOB_NAME} [${env.BUILD_NUMBER}]" """)
		        }
			}
		}
		
		stage("Deploy"){
		    steps {
                sh "ssh -tt jenkins@172.16.10.12 'docker pull phuongsonkma/flask-blog'"
                sh "ssh -tt jenkins@172.16.10.12 'docker stop flask-blog'"
                sh "ssh -tt jenkins@172.16.10.12 'docker rm flask-blog'"
                sh "ssh -tt jenkins@172.16.10.12 'docker run -dp 5000:5000 --name=flask-blog phuongsonkma/flask-blog'"
                sh "ssh -tt jenkins@172.16.10.12 'docker image prune -af'"
            }
            post {
				success {
				   slackSend (color: 'good', message: """SUCCESS: Job "${env.STAGE_NAME} ${env.JOB_NAME} [${env.BUILD_NUMBER}]" Check out websites: http://172.16.10.12:5000 """)
		        }
		        failure {
		           slackSend (color: 'danger', message: """FAIL: Job "${env.STAGE_NAME} ${env.JOB_NAME} [${env.BUILD_NUMBER}]" """)
		        }
			}
		}
	}

	post {
		always {
			sh 'docker logout'
			sh 'rm -rf /home/jenkins/workspace/flask-blog/flask-blog'
			sh "ssh -tt jenkins@172.16.10.12 'docker image prune -af'"
		}
		success {
		   slackSend (color: 'good', message: """SUCCESS: Job "${env.STAGE_NAME} ${env.JOB_NAME} [${env.BUILD_NUMBER}]" """)
        }
        failure {
           slackSend (color: 'danger', message: """FAIL: Job "${env.STAGE_NAME} ${env.JOB_NAME} [${env.BUILD_NUMBER}]" """)
        }
	}

}
