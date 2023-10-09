from fastapi import status, HTTPException


def EntitiesNotFound(Entities: str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"sorry, {Entities} not found")

def NotCreatedEntity(Entity: str):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"an error ocurred while creating the entity {Entity}")

def CouldNotAssociateEntities(entity_one: str, entity_two: str):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"could not associate entities with id {entity_one} and {entity_two}")

def UnauthorizedException():
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="INACTIVATE", headers={"WWW-Authenticate"})

def InactivateUser():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INACTIVATE_USER")




