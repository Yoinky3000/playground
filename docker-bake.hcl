ABC = ABC != "" ? ABC : "ssssss"

target "default" {
    dockerfile = "./Dockerfile"
    args = {
        CUR = "${ABC}"
    }
}