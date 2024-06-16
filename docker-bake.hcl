target "default" {
    dockerfile = "./Dockerfile"
    args = {
        TEST = "${ABC}"
    }
}