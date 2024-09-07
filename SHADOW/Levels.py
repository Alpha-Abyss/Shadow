import pygame
import json
import os

class JSONMapLoader:
    def __init__(self, filename):
        # Load the JSON map data
        with open(filename, 'r') as file:
            self.map_data = json.load(file)

        self.tilewidth = self.map_data['tilewidth']
        self.tileheight = self.map_data['tileheight']
        self.tilesets = self.map_data['tilesets']

        # Load tileset images
        self.tileset_images = []
        for tileset in self.tilesets:
            tileset_image_path = os.path.join(os.path.dirname(filename), tileset['image'])
            tileset_image = pygame.image.load(tileset_image_path)
            self.tileset_images.append(tileset_image)

        # Determine the number of columns in each tileset
        self.tileset_columns = [image.get_width() // tileset['tilewidth'] for image, tileset in zip(self.tileset_images, self.tilesets)]

    def get_tile_image(self, gid):
        if gid == 0:
            return None

        # Find the correct tileset for the given GID
        tileset_index = 0
        for i, tileset in enumerate(self.tilesets):
            if gid >= tileset['firstgid']:
                tileset_index = i

        gid -= self.tilesets[tileset_index]['firstgid']  # Adjust GID to local tileset GID
        tileset_image = self.tileset_images[tileset_index]
        tilewidth = self.tilesets[tileset_index]['tilewidth']
        tileheight = self.tilesets[tileset_index]['tileheight']
        columns = self.tileset_columns[tileset_index]

        # Calculate the position of the tile in the tileset image
        tile_x = gid % columns
        tile_y = gid // columns
        rect = pygame.Rect(tile_x * tilewidth, tile_y * tileheight, tilewidth, tileheight)
        return tileset_image.subsurface(rect)

    def draw_layer(self, surface, layer, camera_x, camera_y):
        if 'chunks' in layer:
            # Loop through each chunk
            for chunk in layer['chunks']:
                chunk_x, chunk_y = chunk['x'], chunk['y']
                chunk_width, chunk_height = chunk['width'], chunk['height']
                chunk_data = chunk['data']

                # Draw each tile in the chunk
                for y in range(chunk_height):
                    for x in range(chunk_width):
                        gid = chunk_data[y * chunk_width + x]
                        tile_image = self.get_tile_image(gid)
                        if tile_image:
                            tile_x = (chunk_x + x) * self.tilewidth
                            tile_y = (chunk_y + y) * self.tileheight

                            # Apply camera offset
                            tile_x -= camera_x
                            tile_y -= camera_y

                            surface.blit(tile_image, (tile_x, tile_y))

    def draw(self, surface, camera_x, camera_y):
        for layer in self.map_data['layers']:
            if layer['type'] == 'tilelayer':
                self.draw_layer(surface, layer, camera_x, camera_y)