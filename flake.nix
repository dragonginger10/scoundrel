{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/release-26.05";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = ["x86_64-linux" "aarch64-linux"];

      perSystem = {pkgs, ...}: let
        python = pkgs.python314.withPackages (p: with p; [
          typer
          textual
          textual-image
          requests
          loguru
          pillow
        ]);
      in {
        devShells.default = pkgs.mkShellNoCC {
          packages = with pkgs; [
            ruff
            just
            ty
            python
            python314Packages.python-lsp-server
            python314Packages.textual-dev
          ];
        };

      };
    };
}
