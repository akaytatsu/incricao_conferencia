pipeline {
agent any

tools {nodejs "nodenv"}
    stages {

        stage("params"){
            steps{
                script{
                    echo 'Pulling...' + env.BRANCH_NAME
                }
            }
        }

        stage("Code Checkout from BitBucket develop") {
            when {
                expression {
                    return env.GIT_BRANCH == "origin/develop"
                }
            }
            steps {
                git branch: 'develop',
                credentialsId: 'bitbucket', 
                url: 'https://thiagofreitas@bitbucket.org/hypercoding/vert-credito-emergencial.git'
            }
        }
        

        stage("Code Checkout from BitBucket master") {
            when {
                expression {
                    return env.GIT_BRANCH == "origin/master"
                }
            }
            steps {
                git branch: 'master',
                credentialsId: 'bitbucket', 
                url: 'https://thiagofreitas@bitbucket.org/hypercoding/vert-credito-emergencial.git'
            }
        }
        
        stage('docker enviroment') {

            steps {
                
                script{
                    try{

                        sh 'cp -f .env.sample .env'
                        sh 'docker-compose -f docker-compose.yml build'
                        sh 'docker-compose -f docker-compose.yml up -d --no-build'
                        sh 'docker-compose -f docker-compose.yml exec -T app pytest --cov --cov-report xml:coverage.xml'
                        sh 'docker-compose -f docker-compose.yml down'
                    }catch(e){
                        sh 'docker-compose -f docker-compose.yml down'
                        throw e
                    }
                }

            }
        
        }
        

        stage('Code Quality Check via SonarQube') {
            when {
                expression {
                    return env.GIT_BRANCH == "origin/develop"
                }
            }

            steps {
            script {
                def scannerHome = tool 'sonar-scanner';
                withSonarQubeEnv("sonar-hprs") {
                sh "${tool("sonar-scanner")}/bin/sonar-scanner \
                -Dsonar.login=d9909dce330edc0f407a59939e3b009fb527ea87"
                    }
                }
            }
        }

        stage('deploy https://vert-emergencia.dev.hprs.com.br/') {

            when {
                expression {
                    return env.GIT_BRANCH == "origin/develop"
                }
            }

            steps{

                script{
                    withCredentials([sshUserPrivateKey(credentialsId: 'hyperspace-homolog', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'userName')]) {
                        
                        def remote = [:]
                        remote.name = "dev-hyperspace"
                        remote.host = "ec2-3-226-71-96.compute-1.amazonaws.com"
                        remote.allowAnyHosts = true

                        remote.user = userName
                        remote.identityFile = identity

                        sshCommand remote: remote, command: 'bash /home/ubuntu/deploy/deploy_vert_emergencial.sh'
                        
                    }
                }

            }

        }

        stage('deploy https://vert-emergencia.hprs.com.br/') {

            when {
                expression {
                    return env.GIT_BRANCH == "origin/master"
                }
            }

            steps{

                script{
                    withCredentials([sshUserPrivateKey(credentialsId: 'hyperspace-homolog', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'userName')]) {
                        
                        def remote = [:]
                        remote.name = "dev-hyperspace"
                        remote.host = "ec2-3-226-71-96.compute-1.amazonaws.com"
                        remote.allowAnyHosts = true

                        remote.user = userName
                        remote.identityFile = identity

                        sshCommand remote: remote, command: 'bash /home/ubuntu/deploy/deploy_vert_emergencial_homolog.sh'
                        
                    }
                }

            }

        }

    }
}
