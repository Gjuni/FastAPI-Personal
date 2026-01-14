CREATE TABLE `user` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL COMMENT '이름',
    `email` VARCHAR(50) NOT NULL COMMENT '이메일',
    `logout` BOOLEAN NOT NULL DEFAULT 0 COMMENT '로그아웃 여부 1: 로그아웃',
    `outDate` DATE NULL COMMENT '로그아웃 시작 일자 : 5일 후에 완전 삭제',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `refreshToken` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `userId` INT NOT NULL COMMENT 'user 테이블 참조',
    `refresh` VARCHAR(500) NOT NULL COMMENT 'Refresh 토큰',
    `access` VARCHAR(500) NOT NULL COMMENT 'Access 토큰',
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_user_refresh` 
        FOREIGN KEY (`userId`) REFERENCES `user` (`id`) 
        ON DELETE CASCADE -- 유저 삭제 시 토큰도 자동 삭제
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `thread` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `userId` INT NOT NULL COMMENT '작성자 ID (이미지의 id2)',
    `title` VARCHAR(500) NOT NULL DEFAULT 'title' COMMENT '제목',
    `body` TEXT NOT NULL COMMENT '내용',
    `date` DATE NOT NULL COMMENT '작성 일',
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_user_thread` 
        FOREIGN KEY (`userId`) REFERENCES `user` (`id`) 
        ON DELETE CASCADE -- 유저 삭제 시 작성한 글도 자동 삭제
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;