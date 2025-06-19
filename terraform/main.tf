provider "render" {
  api_key = var.render_api_key
}

resource "render_service" "webhook" {
  name        = var.service_name
  type        = "web_service"
  repo        = var.repo_url
  branch      = "main"
  env         = "docker"
  plan        = "free"
  auto_deploy = true
}
