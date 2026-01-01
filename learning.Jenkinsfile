pipeline {
    agent {
        label 'built-in'
    }

    environment {
        // Using the internal Podman gateway to find the Mosquitto container
        MQTT_BROKER = 'host.containers.internal'
    }

    stages {
        stage('1. Environment Setup') {
            steps {
                echo "Creating Virtual Environment and installing dependencies..."
                // Creates a local 'venv' folder and installs requirements 
                bat '''
                python -m venv venv
                .\\venv\\Scripts\\pip install -r requirements.txt
                '''
            }
        }

        stage('2. Provision Broker') {
            steps {
                echo "Ensuring Mosquitto Broker is running..."
                // This starts the broker container using the podman installed in your agent
                bat 'podman run -d --name mqtt-broker -p 1883:1883 eclipse-mosquitto || exit 0'
            }
        }

        stage('3. Integration Testing') {
            parallel {
                stage('Device Simulation') {
                    steps {
                        echo "Starting Device Simulator from subfolder..."
                        // Added 1-minute timeout to stop the 'while True' loop eventually 
                        timeout(time: 1, unit: 'MINUTES') {
                            bat ".\\venv\\Scripts\\python.exe simulator/iot_device_simulator.py --broker %MQTT_BROKER%"
                        }
                    }
                }
                stage('Pytest Logic') {
                    steps {
                        echo "Running Pytest from subfolder..."
                        // Points to the exact folder: iot-testbed/tests/pytest 
                        bat ".\\venv\\Scripts\\python.exe -m pytest tests/pytest --junitxml=results.xml"
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Generating Test Reports..."
            // Looks for the results.xml generated in the workspace 
            junit 'results.xml'
        }
        cleanup {
            echo "Cleaning up containers..."
            sh 'podman stop mqtt-broker || true'
            sh 'podman rm mqtt-broker || true'
        }
    }
}