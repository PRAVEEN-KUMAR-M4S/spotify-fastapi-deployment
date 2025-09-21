
import uuid
import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Form, UploadFile
from fastapi.params import Depends, File
from sqlalchemy.orm import Session,joinedload
from database import get_db
from middleware.auth_middle_ware import auth_middleware
from models.faviroute import Faviroute
from models.song import Song
from pydantic_schema.faviroute_songs import FavirouteSongs


router=APIRouter()

# Configuration       
cloudinary.config( 
    cloud_name = "dkzykrs4s", 
    api_key = "994823231368849", 
    api_secret = "AuhriDLr0B8iR0KzYhwleX9MgX0", # Click 'View API Keys' above to copy your API secret
    secure=True
)

@router.post('/upload',status_code=201)
def upload_song(song:UploadFile=File(...), thumbnail:UploadFile=File(...), artist:str=Form(...), song_name:str=Form(...), hex_code:str=Form(...),db:Session=Depends(get_db),auth_dic=Depends(auth_middleware)):
    song_id=str(uuid.uuid4())
    song_res=cloudinary.uploader.upload(song.file, resource_type="auto", folder=f"songs/{song_id}")
    thumbnail_res=cloudinary.uploader.upload(thumbnail.file, resource_type="image", folder=f"songs/{song_id}")

    new_song=Song(
        id=song_id,
        artist=artist,
        song_name=song_name,
        hex_code=hex_code,
        song_url=song_res['secure_url'],
        thumbnail_url=thumbnail_res['url']
    )

    db.add(new_song)
    db.commit()
    db.refresh(new_song)

    return {"message": "Song uploaded successfully", "song": new_song}

@router.get('/list')
def list_song(db: Session=Depends(get_db),auth_dic=Depends(auth_middleware)):
    songs = db.query(Song).all()
    return {"songs": songs}
@router.post('/favorite')
def favorite_song(fav:FavirouteSongs,db:Session=Depends(get_db),auth_dic=Depends(auth_middleware)):
    print(auth_dic)
    user_id=auth_dic['uid']
    fav_song=db.query(Faviroute).filter(Faviroute.song_id==fav.song_id,Faviroute.user_id==user_id).first()

    print(fav_song)

    if fav_song:
        db.delete(fav_song)
        db.commit()
        return {"message":False}
    else:
        new_fav=Faviroute(
            id=str(uuid.uuid4()),
            song_id=fav.song_id,
            user_id=user_id
        )
        db.add(new_fav)
        db.commit()
        db.refresh(new_fav)
        return {"message":True}
    pass


@router.get('/list/favorite')
def list_favorite_songs(db: Session=Depends(get_db),auth_dic=Depends(auth_middleware)):
    user_id=auth_dic['uid']
    fav_songs=db.query(Faviroute).filter(Faviroute.user_id==user_id).options(joinedload(Faviroute.song),joinedload(Faviroute.user)).all()
    return fav_songs