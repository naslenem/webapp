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
          stage("Code coverage") {
               steps {
                    script {
                    sh 'coverage report --data-file=cov.xml'
                    publishHTML (target: [
                    	reportDir: '.',
                    	reportFiles: 'cov.xml',
                    	reportName: "report"
                    	])
                    

                    }
               }
          }
    }
}
