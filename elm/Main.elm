module App where

import Graphics.Element (..)
import Text
import Http (..)
import Signal (..)


display : Response String -> Element
display response =
    case response of
      Success info -> Text.asText info
      Waiting -> Text.asText "Waiting"
      Failure _ _ -> Text.asText "Failure"

response : Signal (Response String)
response =
    sendGet (constant "/api/v1/user/?format=json")

main = map display response
