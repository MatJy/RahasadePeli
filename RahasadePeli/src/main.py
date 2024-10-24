# TEE PELI TÄHÄN
import pygame
import random


class Rahasade:
    def __init__(self):
        pygame.init()

        self.lataa_kuvat()
        self.leveys, self.korkeus = 600, 500

        self.x = 0
        self.y = self.korkeus - self.roboKorkeus
        self.kolikot = []
        self.hirviot = []
        self.pisteet = 0

        self.fontti = pygame.font.SysFont("Arial", 24)

        self.spawn_timer = 0
        self.spawn_interval = random.randint(30, 60)

        self.oikealle = False
        self.vasemmalle = False

        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))

        self.kello = pygame.time.Clock()

        self.silmukka()

    def lataa_kuvat(self):
        self.robo = pygame.image.load('robo.png')
        self.kolikko = pygame.image.load('kolikko.png')
        self.hirvio = pygame.image.load('hirvio.png')

        self.roboKorkeus = self.robo.get_height()
        self.roboLeveys = self.robo.get_width()

        self.kolikkoKorkeus = self.kolikko.get_height()
        self.kolikkoLeveys = self.kolikko.get_width()

        self.hirvioKorkeus = self.hirvio.get_height()
        self.hirvioLeveys = self.hirvio.get_width()

    def uusi_peli(self):
        self.pisteet = 0
        self.kolikot = []
        self.hirviot = []

    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.piirra_naytto()
            self.paivita_tippuvat()
            self.keraa_kolikko()

            self.kello.tick(60)

    def tutki_tapahtumat(self):

        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = True

                if self.peli_loppu():
                    if tapahtuma.key == pygame.K_F2:
                        self.uusi_peli()
                    if tapahtuma.key == pygame.K_ESCAPE:
                        exit()

            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False

            if tapahtuma.type == pygame.QUIT:
                exit()
        if self.peli_loppu():
            return

        if self.oikealle and self.x + self.roboLeveys < 600:
            self.x += 5
        if self.vasemmalle and self.x > 0:
            self.x -= 5

    def luo_kolikko(self):
        x = random.randint(0, self.leveys - self.kolikkoLeveys)
        self.kolikot.append({'x': x, 'y': 0 - self.kolikkoKorkeus})

    def luo_hirvio(self):
        x = random.randint(0, self.leveys - self.hirvioLeveys)
        self.hirviot.append({'x': x, 'y': 0 - self.hirvioKorkeus})

    def paivita_tippuvat(self):
        if self.peli_loppu():
            return
        self.spawn_timer += 1

        if self.spawn_timer >= self.spawn_interval:
            kuvat = [self.luo_kolikko, self.luo_hirvio]
            kumpi = random.randint(0, 1)
            kuvat[kumpi]()
            self.spawn_timer = 0
            self.spawn_interval = random.randint(30, 60)

        for kolikko in self.kolikot:
            kolikko['y'] += 4
        for hirvio in self.hirviot:
            hirvio['y'] += 4

        self.kolikot = [
            kolikko for kolikko in self.kolikot if kolikko['y'] < self.korkeus]
        self.hirviot = [
            hirvio for hirvio in self.hirviot if hirvio['y'] < self.korkeus]

    def peli_loppu(self):
        for hirvio in self.hirviot:
            if self.x < hirvio['x'] + self.hirvioLeveys and self.x + self.roboLeveys > hirvio['x']:
                if self.y < hirvio['y'] + self.hirvioKorkeus and self.y + self.roboKorkeus > hirvio['y']:
                    return True
        return False

    def keraa_kolikko(self):
        for kolikko in self.kolikot:
            if self.x < kolikko['x'] + self.hirvioLeveys and self.x + self.roboLeveys > kolikko['x']:
                if self.y < kolikko['y'] + self.hirvioKorkeus and self.y + self.roboKorkeus > kolikko['y']:
                    self.pisteet += 1
                    del self.kolikot[self.kolikot.index(kolikko)]

    def piirra_naytto(self):
        self.naytto.fill((255, 255, 255))

        self.naytto.blit(
            self.robo, (self.x, self.korkeus - self.roboKorkeus))

        for kolikko in self.kolikot:
            self.naytto.blit(self.kolikko, (kolikko['x'], kolikko['y']))

        for hirvio in self.hirviot:
            self.naytto.blit(self.hirvio, (hirvio['x'], hirvio['y']))

        teksti = self.fontti.render(
            "Pisteet: " + str(self.pisteet), True, (255, 0, 0))
        self.naytto.blit(teksti, (self.leveys - 100, 10))

        if self.peli_loppu():
            teksti = self.fontti.render(
                "Osuit hirviöön, hävisit!", True, (255, 0, 0))
            teksti_x = self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.korkeus / 2 - teksti.get_height() / 2
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x,
                             teksti_y, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (teksti_x, teksti_y))

            teksti = self.fontti.render("Uusi peli = F2", True, (255, 0, 0))
            teksti_y = self.korkeus - 222
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x,
                             teksti_y, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (teksti_x, teksti_y))

            teksti = self.fontti.render(
                "Poistu pelistä = ESC", True, (255, 0, 0))
            teksti_y = self.korkeus - 194
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x,
                             teksti_y, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (teksti_x, teksti_y))

        pygame.display.flip()


if __name__ == "__main__":
    Rahasade()
