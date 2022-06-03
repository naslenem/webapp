pipeline {
     agent {
          docker {
               image: python-image:3
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
                    sh 'python3 manage.py test -v 2'
                    step([$class: 'CoberturaPublisher', 
                        coberturaReportFile: "cov.xml",
                    ])
                    junit "pyunit.xml"
                    }
               }
          }
    }
}
