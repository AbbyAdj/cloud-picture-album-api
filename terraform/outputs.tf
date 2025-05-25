output "token" {
  value = nonsensitive(module.secrets.github_token)

}