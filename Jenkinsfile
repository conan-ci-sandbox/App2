user_channel = "mycompany/stable"
config_url = "https://github.com/conan-ci-cd-training/settings.git"
conan_develop_repo = "conan-develop"
conan_tmp_repo = "conan-tmp"
artifactory_metadata_repo = "conan-metadata"

artifactory_url = (env.ARTIFACTORY_URL != null) ? "${env.ARTIFACTORY_URL}" : "jfrog.local"

def profiles = [
  "debug-gcc6": "conanio/gcc6",	
  "release-gcc6": "conanio/gcc6"	
]

def get_stages(profile, docker_image) {
    return {
        stage(profile) {
            node {
                docker.image(docker_image).inside("--net=host") {
                    def scmVars = checkout scm
                    withEnv(["CONAN_USER_HOME=${env.WORKSPACE}/conan_cache"]) {
                        def lockfile = "${profile}.lock"
                        try {
                            stage("Configure Conan") {
                                sh "conan --version"
                                sh "conan config install ${config_url}"
                                sh "conan remote add ${conan_develop_repo} http://${artifactory_url}:8081/artifactory/api/conan/${conan_develop_repo}" // the namme of the repo is the same that the arttifactory key
                                sh "conan remote add ${conan_tmp_repo} http://${artifactory_url}:8081/artifactory/api/conan/${conan_tmp_repo}" // the namme of the repo is the same that the arttifactory key
                                withCredentials([usernamePassword(credentialsId: 'artifactory-credentials', usernameVariable: 'ARTIFACTORY_USER', passwordVariable: 'ARTIFACTORY_PASSWORD')]) {
                                    sh "conan user -p ${ARTIFACTORY_PASSWORD} -r ${conan_develop_repo} ${ARTIFACTORY_USER}"
                                    sh "conan user -p ${ARTIFACTORY_PASSWORD} -r ${conan_tmp_repo} ${ARTIFACTORY_USER}"
                                }
                            }

                           stage("Create package") {                                
                                sh "conan graph lock . --profile ${profile} --lockfile=${lockfile} -r ${conan_develop_repo}"
                                sh "cat ${lockfile}"
                                sh "conan create . ${user_channel} --profile ${profile} --lockfile=${lockfile} -r ${conan_develop_repo} --ignore-dirty"
                                sh "cat ${lockfile}"
                            }

                            if (env.BRANCH_NAME == "develop") {                     
                                stage("Upload package") {
                                    sh "conan upload '*' --all -r ${conan_develop_repo} --confirm"
                                }
                            } 

                            stage("Upload lockfile") {
                                if (env.BRANCH_NAME == "develop") {
                                    def name = sh (script: "conan inspect . --raw name", returnStdout: true).trim()
                                    def version = sh (script: "conan inspect . --raw version", returnStdout: true).trim()                                
                                    def lockfile_url = "http://${artifactory_url}:8081/artifactory/${artifactory_metadata_repo}/${env.JOB_NAME}/${env.BUILD_NUMBER}/${name}/${version}@${user_channel}/${profile}/conan.lock"
                                    withCredentials([usernamePassword(credentialsId: 'artifactory-credentials', usernameVariable: 'ARTIFACTORY_USER', passwordVariable: 'ARTIFACTORY_PASSWORD')]) {
                                        sh "curl --user \"\${ARTIFACTORY_USER}\":\"\${ARTIFACTORY_PASSWORD}\" -X PUT ${lockfile_url} -T ${lockfile}"
                                    }                                
                                }
                            }
                        }
                        finally {
                            deleteDir()
                        }
                    }
                }
            }
        }
    }
}

pipeline {
    agent none
    stages {
        stage('Build') {
            steps {
                script {
                    echo("${currentBuild.fullProjectName.tokenize('/')[0]}")
                    withEnv(["CONAN_HOOK_ERROR_LEVEL=40"]) {
                        parallel profiles.collectEntries { profile, docker_image ->
                            ["${profile}": get_stages(profile, docker_image)]
                        }
                    }                 
                }
            }
        }
    }
}