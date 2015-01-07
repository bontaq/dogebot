module App where

import Graphics.Element (..)
import Text
import Http (..)
import Signal as Signal
import Html
import Time (..)
import Json.Decode ((:=), object3, string, list, at, decodeString, Decoder)
import List (..)


type alias User =
    { user_name: String
    , user_id: String
    , balance: String }

type alias State =
    { users: List User
    , test: Element }

display : Response String -> Decoder a -> Element
display response decoder =
    case response of
      Success info -> Text.asText <| decodeString decoder info
      Waiting -> Text.asText "Waiting"
      Failure _ _ -> Text.asText "Failure"

responseUser : Signal (Response String)
responseUser = sendGet (Signal.map (always "/api/v1/user/?format=json") (every (5 * second)))

responseMessage : Signal (Response String)
responseMessage = sendGet (Signal.map (always "/api/v1/message/?format=json") (every (10 * second)))

-- displayUser response =
--     case response of
--       Success info -> Text.asText <| decodeString decodeUsers info
--       Waiting -> Text.asText "Waiting"
--       Failure _ _ -> Text.asText "Failure"

-- do the names have to be the same?
decodeUser : Decoder User
decodeUser = object3 User ( "user_name" := string )
                          ( "user_id" := string )
                          ( "balance" := string )

decodeUsers : Decoder (List User)
decodeUsers = at ["objects"] (list decodeUser)

-- display2 a b = flow down
--                <| map display [a, b]

-- main : Signal Element
-- main = Signal.map2 display2 responseUser responseMessage

display2 = Signal.map2 display responseUser (Signal.constant decodeUsers)

--main = foldp
