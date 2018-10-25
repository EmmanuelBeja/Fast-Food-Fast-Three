logout = () => {
  sessionStorage.clear();
  location.replace("/login");
}
