export const uiState = $state({
  isSearchOpen: false,
  openSearch() {
    this.isSearchOpen = true;
  },
  closeSearch() {
    this.isSearchOpen = false;
  },
});
