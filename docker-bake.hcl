target "default" {
    dockerfile = "./Dockerfile"
    args = {
        CUR = "${ABC}"
        PREV = "${PREVIOUS}"
    }
}