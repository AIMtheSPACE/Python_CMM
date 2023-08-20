import pygame
import sys
from random import randint
from main import *
from defi import*
# --------------------------------- 여러 Class 설정 ---------------------------------



# --------------------------------- setting ---------------------------------
pygame.init() # 초기화
pygame.display.set_caption("러브캐처 인 청운") # 화면 이름
pygame.display.set_icon(pygame.image.load("Image/청운 로고.png") )

game = Game()
# --------------------------------- 여러 함수 설정 ---------------------------------


# --------------------------------- 메인 이벤트 함수 ---------------------------------
while True:
    if True:
        current_time = pygame.time.get_ticks() // 1000  # 현재 시간(초) 가져오기
        screen.fill('#71ddee')

        for event in pygame.event.get(): # 종류 및 키 값 받아오기 등
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_image == "main":
                        current_image = "intro"  # 이미지 변경

                elif event.key == pygame.K_p:
                    show_settings_overlay = not show_settings_overlay

                elif event.key == pygame.K_l:
                    show_checklist_overlay = not show_checklist_overlay
                    show_right_arrow = not show_right_arrow
                    show_left_arrow = not show_left_arrow

                elif event.key == pygame.K_SEMICOLON:
                    page = adjust_value(page, 1, 1, 4)

                elif event.key == pygame.K_k:
                    page = adjust_value(page, -1, 1, 4)

        if current_image == "main": # 메인 이미지 노출
            draw_scaled_image(main_image, 0.9, (screen.get_width() // 2, screen.get_height() // 2))
            

        elif current_image == "intro": # 인트로 이미지 노출
            intro_image = pygame.image.load('Image/intro.png').convert_alpha()
            intro_image_rect = intro_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(intro_image, intro_image_rect.topleft)
            
            # 스페이스바를 눌렀을 때 이미지 변경
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        show_settings_overlay = not show_settings_overlay

                    elif event.key == pygame.K_SPACE:
                        current_image = "game"  # 이미지 변경
                        countdown_start_time = current_time  # 카운트다운 시작 시간 설정

                # 세팅 버튼 구현
            if setting_button.draw(screen) or (show_settings_overlay and event.type == pygame.KEYDOWN and event.key == pygame.K_p):
                show_settings_overlay = not show_settings_overlay

            if show_settings_overlay:
                draw_settings_overlay(screen, font)
                draw_endgame_overlay(screen)

        # 메인 게임 플레이 시
        elif current_image == "game":

            if setting_button.draw(screen) or (show_settings_overlay and event.type == pygame.KEYDOWN and event.key == pygame.K_p):
                show_settings_overlay = not show_settings_overlay

            if show_settings_overlay:
                draw_settings_overlay(screen, font)
                draw_endgame_overlay(screen)

            if menu_button.draw(screen): # 메뉴 임시 설정
                pygame.quit()
                sys.exit()

            # 체크리스트 띄우는 코드
            if checklist_button.draw(screen) or (show_checklist_overlay and event.type == pygame.KEYDOWN and event.key == pygame.K_l):
                # 체크리스트 노출
                show_checklist_overlay = not show_checklist_overlay
                # 화살표 노출
                show_right_arrow = not show_right_arrow
                show_left_arrow = not show_left_arrow

            if show_checklist_overlay:
                overlay_color = (0, 0, 0, 128)
                overlay_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                overlay_surface.fill(overlay_color)
                screen.blit(overlay_surface, (0, 0))

                # 선 표시
                if page == 1:
                    draw_scaled_image(bigchecklist1_image, 0.5, (screen.get_width() // 2, screen.get_height() // 2))
                elif page == 2:
                    draw_scaled_image(bigchecklist2_image, 0.5, (screen.get_width() // 2, screen.get_height() // 2))
                elif page ==3:
                    draw_scaled_image(bigchecklist3_image, 0.5, (screen.get_width() // 2, screen.get_height() // 2))
                elif page ==4:
                    draw_scaled_image(bigchecklist4_image, 0.5, (screen.get_width() // 2, screen.get_height() // 2))
            
            if show_right_arrow and rightarrow_button.draw(screen):
                page = adjust_value(page, 1, 1, 5)

            if show_left_arrow and leftarrow_button.draw(screen):
                page = adjust_value(page, -1, 1, 5)

            #잘 카운트 되는지 알아보기 위한 코드 나중에 삭제
            draw_text(str(page), font, TEXT_COL, screen.get_width() - 50, screen.get_height() - 50)

            # 카운트 다운 시작
            if countdown_start_time is not None:
                remaining_time = countdown_duration - (current_time - countdown_start_time)
                if remaining_time > 0:
                    if period == 4:
                        countdown_text = f"Lunch Time / Time left : {remaining_time // 60:02}:{remaining_time % 60:02}"
                        countdown_font = pygame.font.SysFont("arialblack", 20)
                        countdown_surface = countdown_font.render(countdown_text, True, TEXT_COL)
                        countdown_rect = countdown_surface.get_rect(topright=(screen.get_width() - 10, 10))
                        screen.blit(countdown_surface, countdown_rect)
                    else:
                        display_countdown(period, screen, remaining_time)

                # 게임 끝 엔딩 화면으로 전환 -> 다른 곳으로 전환 되도록 바꿀 것
                if remaining_time == 0:
                    current_image = "classtime" 
                    period += 1

            # 커플 버튼 값 변경
            if couple1_button.draw(screen):
                page1couple[0] = 1

            # [커플코드] 체크 리스트 선 show or not (앞에서 누르면 함수값 1로 바꾸어 주는 거 필요)
            if show_checklist_overlay:
                for page_index, couple_list in enumerate([page1couple, page2couple, page3couple, page4couple], start=1):
                    if page == page_index:
                        for couple_index, couple_value in enumerate(couple_list):
                            if couple_value == 1:
                                draw_checklist_line_image(page, couple_index)
            
        elif current_image == "end": # 게임 엔딩 화면
            end_image = pygame.image.load('Image/ending.png').convert_alpha()
            end_image_rect = end_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(end_image, end_image_rect.topleft)
        
        

        # 쉬는 시간 설정
        if current_image == "classtime":
            if classtime_button.draw(screen):
                current_image = "game"
                if period == 4:
                    countdown_start_time = current_time + 10 # 점심 시간 조절
                elif period == 7:
                    current_image = "end"
                else:
                    countdown_start_time = current_time
    if current_image == "game":
        tilemap = maps.world_1.stage_1
        game = Game()
        game.new(tilemap)
        game.main()
        for event in pygame.event.get(): # 종류 및 키 값 받아오기 등
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


    pygame.display.update()
    clock.tick(60)
