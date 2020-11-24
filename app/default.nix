{ lib
, buildPythonPackage
, requests_oauthlib
, python-telegram-bot
, urllib3
}:

buildPythonPackage {
  name = "queuebot";

  src = lib.cleanSourceWith {
    filter = name: type: let baseName = baseNameOf (toString name); in !lib.hasSuffix ".nix" baseName;
    src = lib.cleanSource ./.;
  };

  propagatedBuildInputs = [
    requests_oauthlib
    python-telegram-bot
    urllib3
  ];

  nativeBuildInputs = [ ];
}
