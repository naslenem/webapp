pipeline {
     agent {
          docker {
               image "python-image:3"
     	  }
     }
     triggers {
          pollSCM('* * * * *')
     }
     stages {
          stage("Compile") {
               steps {
                    sh "./test.sh"
               }
          }
          stage("Unit test") {
               steps {
                    sh "./test.sh"
               }
          }
          stage('Initialize'){
          steps {
                            def dockerHome = tool 'Docker'
        env.PATH = "${dockerHome}/bin:${env.PATH}"
               }

    }
          stage("Code coverage") {
               steps {
                    script {
                    sh 'coverage run --data-file="cov.xml" manage.py test'
                    publishHTML (target: [
                    	reportDir: '.',
                    	reportFiles: 'cov.xml',
                    	reportName: "report"
                    	])
                    

                    }
               }
          }
          stage("Docker build") {
          
          	steps {
          	     sh "docker build -t localhost:5000/python-image ."
          	}
          }
    }
}
